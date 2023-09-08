import traceback, json
from prompt_toolkit.layout.containers import AnyContainer, Container, VerticalAlign

from prompt_toolkit.layout.dimension import AnyDimension, Dimension

import pypatch, textwrap, help
pypatch.patch()

import discord
from typing import Callable, Sequence, TypeVar, Generic
import asyncio
from rich.traceback import install
install(show_locals=True)
import discord.utils
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, Window, HSplit, VSplit, ScrollablePane, FormattedTextControl, WindowAlign, BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase, KeyPressEvent


_KT = TypeVar("_KT",contravariant=True)
_VT = TypeVar("_VT",contravariant=True)
    
class DefaultDict(dict, Generic[_KT,_VT]):
    def __init__(self, map, default:_VT = None):
        super().__init__(map)
        self.default_value = default

    def __getitem__(self, __key: _KT) -> _VT: # pyright: ignore
        try:
            return super().__getitem__(__key)
        except KeyError: return self.default_value
    
    def __setitem__(self, __key: _KT, __value: _VT) -> None:
        super().__setitem__(__key, __value)
        json.dump(self, open('dict',"w"))
# session states
mode = 0 # 0 for cmd, 1 for input, 2 for scrolling
scrollTarget = ""
scrollCursorPos = DefaultDict[str,int]({},0)
focusingG = 0
focusingCh = 0
guilds = []
channels = []
messages = []

def render_guilds(x=0):
    global guilds, windows
    guilds = [(i.name, i.id) for i in client.guilds]
    gwin = windows["guilds"] 
    container = []
    for i in guilds:
        container.append(Window(FormattedTextControl(i[0]),width=12,height=1))
    # gwin.refresh(0,0,x,0,curses.LINES-1+x,9)
    gwin.content.children = container # pyright: ignore
    app._redraw()

async def render_channels(gid:int):
    global channels, windows
    h = await discord.utils.get_or_fetch(client,"guild",id=gid)
    ch = [(i.type, i.name,i.id,i.position) for i in h.channels] # pyright: ignore
    cwin = windows["channels"]
    container = [Window()]*len(ch)
    channels = [(1,"2",3,4)]*len(ch)
    for i in ch:
        chIcon = ""
        match i[0].value:
            case 0: chIcon = "\uf4df"
            case 1: chIcon = "\uf456"
            case 2: chIcon = "\ue638"
            case 4: chIcon = "\U000f035d"
            case 5: chIcon = "\U000f00e6"
            case 10 | 11 | 12: chIcon = "\u251c"
            case 13: chIcon = "\U000f1749"
            case 15: chIcon = "\U000f028c"
        
        if "music" in i[1]: chIcon = "\U000f02cb"
        container[i[3]] = Window(FormattedTextControl(chIcon+" "+i[1]),width=22,height=1)
        channels[i[3]] = i

    cwin.content.children = container # pyright: ignore
    app._redraw()

async def render_messages(cid:int):
    global messages, windows
    stfupyright: discord.TextChannel = await discord.utils.get_or_fetch(client, "channel", cid) # pyright: ignore
    messages = [(i.id, i.author.color.__str__(), i.author.name, i.created_at, i.content) async for i in stfupyright.history(limit = 50)]
    container = []
    lastUser = 0
    for i in messages:
        h=HSplit([
            Window(FormattedTextControl(i[4],focusable=True),wrap_lines=True)
        ])
        if i[0] != lastUser:
            h.children.insert(0, VSplit([
                Window(FormattedTextControl(i[2],"fg:"+i[1])),
                Window(FormattedTextControl(i[3].strftime("%m/%d/%Y, %H:%M:%S"),"fg:gray"))
            ],height=1))
        container.insert(0, h)
        lastUser = i[0]
    mwin = windows["messageContent"]
    mwin.content.children = container # pyright: ignore
    app.layout.focus(container[-1])
    app._redraw()

def keybind_lore():
    kb = KeyBindings()

    @kb.add("s","g", filter=Condition(lambda: mode == 0))
    def scrollGuild(e: KeyPressEvent):
        global scrollTarget, mode
        scrollTarget = "guilds"
        mode = 2
        windows[scrollTarget].content.get_children()[scrollCursorPos[scrollTarget]].style = tc.selectHighlight # pyright: ignore

    @kb.add("s","c", filter=Condition(lambda:len(channels)!=0))
    def scrollChannel(e: KeyPressEvent):
        global scrollTarget, mode
        scrollTarget = "channels"
        mode = 2
        st = scrollTarget+"_"+str(focusingG)
        windows[scrollTarget].content.get_children()[scrollCursorPos[st]].style = tc.selectHighlight # pyright: ignore

    @kb.add("s","m", filter=Condition(lambda:len(messages)!=0))
    def scrollMessages(e: KeyPressEvent):
        global scrollTarget, mode
        scrollTarget = "messageContent"
        mode = 2
        st = scrollTarget+"_"+str(focusingCh)
        windows[scrollTarget].content.get_children()[scrollCursorPos[st]].style = tc.msgFocusHighlight # pyright: ignore

    def sup(e: KeyPressEvent):
        global focusingG
        st = scrollTarget+("" if scrollTarget == "guilds" else "_"+str(focusingG))
        if (i:=scrollCursorPos[st]-1) >= 0:
            win = windows[scrollTarget].content.get_children()
            limbo = win[i]
            un = win[i+1]
            un.style = "" # pyright: ignore
            limbo.style = tc.selectHighlight if scrollTarget != "messageContent" else tc.msgFocusHighlight # pyright: ignore
            scrollCursorPos[st]-=1
            app.layout.focus(limbo)
    kb.add("up", filter=Condition(lambda: scrollTarget != ""))(sup)
    kb.add("<scroll-up>", filter=Condition(lambda: scrollTarget != ""))(sup)

    def sdown(e: KeyPressEvent):
        global focusingG
        st = scrollTarget+("" if scrollTarget == "guilds" else "_"+str(focusingG))
        if (i:=scrollCursorPos[st]+1) < len((win:=windows[scrollTarget].content.get_children())):
            win[i].style = tc.selectHighlight if scrollTarget != "messageContent" else tc.msgFocusHighlight # pyright: ignore
            win[i-1].style = "" # pyright: ignore
            scrollCursorPos[st]+=1
            app.layout.focus(win[i])
    kb.add("down", filter=Condition(lambda: scrollTarget != ""))(sdown)
    kb.add("<scroll-down>", filter=Condition(lambda: scrollTarget != ""))(sdown)

    @kb.add("enter")
    async def click(e):
        global mode, scrollTarget, focusingG, focusingCh
        if mode == 2 and scrollTarget == "guilds":
            await render_channels(guilds[scrollCursorPos[scrollTarget]][1])
            windows[scrollTarget].content.get_children()[scrollCursorPos[scrollTarget]].style=""
            focusingG = guilds[scrollCursorPos[scrollTarget]][1]
            scrollTarget = "channels"
        elif mode == 2 and scrollTarget == "channels":
            st = scrollTarget+("" if scrollTarget == "guilds" else "_"+str(focusingG))
            chInfo = channels[scrollCursorPos[st]]
            await render_messages(chInfo[2])
            focusingCh = chInfo[2]
            mode = 0
            scrollTarget=""

    @kb.add("escape", filter=Condition(lambda: mode != 0))
    def ret(e):
        global mode, scrollTarget, focusingG
        if mode == 2:
            windows[scrollTarget].content.get_children()[scrollCursorPos[scrollTarget]].style=""
            if scrollTarget == "guilds":
                mode = 0 
                scrollTarget = ""
            if scrollTarget == "channels": 
                scrollTarget = "guilds"
                focusingG = 0

    @kb.add("c-q")
    async def shut(e: KeyPressEvent):
        e.app.exit()
        await client.close()

    return kb
 

class ThemeColors:
    selectHighlight = "bg:gray fg:black"
    mainBg = "bg:#363940"
    secondaryBg = "bg:#212226"
    msgFocusHighlight = "bg:#2F3238"
tc = ThemeColors()

async def main():
    global windows, client, app, inputBoxes
    conf = help.loadJson("config.json")
    windows = {
        "guilds": ScrollablePane(HSplit([Window()],style=tc.secondaryBg,width=12),show_scrollbar=False),
        "channels":ScrollablePane(HSplit([Window()],width=22,style=tc.mainBg),show_scrollbar=False),
        "messageContent":ScrollablePane(HSplit([Window()],style=tc.mainBg), max_available_height=848940300),
        "VerticalLine": Window(char=" ", style="class:line,vertical-line "+tc.secondaryBg, width=1)
    }
    def t(**kwargs):
        buf = Buffer()
        return (Window(BufferControl(buf),**kwargs), buf)
    inputBoxes = {
        "messageInput": t(height = 2, wrap_lines=True, style = tc.secondaryBg),
    }
    windows["messages"] = HSplit([windows["messageContent"], inputBoxes["messageInput"][0]]) # pyright: ignore
    
    kb = keybind_lore() 

    lay = Layout(HSplit([Window(),Window(FormattedTextControl("Loading Disconsole"), height=2, align=WindowAlign.CENTER)]))
    app = Application(lay,full_screen=True,mouse_support=True, key_bindings=kb)
        
    import platform
    if platform.system() == "Windows":
        from ctypes import windll, pointer, c_ulong
        from ctypes.wintypes import DWORD, HANDLE

        h = DWORD()
        handle = HANDLE(windll.kernel32.GetStdHandle(c_ulong(-10)))
        windll.kernel32.GetConsoleMode(handle, pointer(h))
        windll.kernel32.SetConsoleMode(handle, h.value | 0x0001)
    tent = discord.Intents.all()
    tent.messages = True
    tent.message_content = True
    client = discord.Client(intents=tent)


    @client.event 
    async def on_ready():
        mainw = VSplit([
            windows["guilds"],
            windows["VerticalLine"],
            windows["channels"],
            windows["VerticalLine"],
            windows["messages"]
        ])

        app.layout.container = mainw

        app._redraw()

        render_guilds()

    @client.event
    async def on_message(i: discord.Message):
        if focusingCh == i.channel.id:
            msg = (i.id, i.author.color.__str__(), i.author.name, i.created_at, i.content)
            windows["messageContent"].content.children.insert(0, HSplit([
            VSplit([
                Window(FormattedTextControl(msg[2],"fg:"+msg[1])),
                Window(FormattedTextControl(msg[3].strftime("%m/%d/%Y, %H:%M:%S"),"fg:gray"))
            ],height=1,padding=4,padding_char=""),
            Window(FormattedTextControl(msg[4]),wrap_lines=True)
        ]))
        app.layout.focus(windows["messageContent"].content.children[-1])

    @client.event
    async def on_error(*no, **noo):
        traceback.print_exc(file=open("tb","a"))
    with patch_stdout(): await asyncio.wait([asyncio.create_task(client.start(token=conf["token"])), asyncio.create_task(app.run_async())])# pyright: ignore

asyncio.run(main())
