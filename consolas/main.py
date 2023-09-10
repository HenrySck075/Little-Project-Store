from datetime import datetime
import traceback

from prompt_toolkit.widgets import TextArea

import help

import selfcord
from typing import TypeVar, Generic
import asyncio
from rich.traceback import install
install(show_locals=True)
import help
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, Window, HSplit, VSplit, ScrollablePane, FormattedTextControl, WindowAlign, BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles.pygments import style_from_pygments_cls

_KT = TypeVar("_KT",contravariant=True)
_VT = TypeVar("_VT",contravariant=True)

tc = help.ThemeColors()

class TypingList(list):
    def __init__(self, *ok):
        super().__init__(*ok)

    def __setitem__(self, k: int, v: selfcord.User | selfcord.Member):
        list.__setitem__(self,k,v)
class DefaultDict(dict, Generic[_KT,_VT]):
    def __init__(self, map, default:_VT = None):
        super().__init__(map)
        self.default_value = default

    def __getitem__(self, __key: _KT) -> _VT: # pyright: ignore
        try:
            return super().__getitem__(__key)
        except KeyError: return self.default_value
# session states
mode = 0 # 0 for cmd, 1 for input, 2 for scrolling
scrollTarget = ""
scrollCursorPos = DefaultDict[str,int]({},0)
focusingG = 0
focusingCh = 0
lastUser = 0
guilds = []
channels = []
messages = []
userColorsCache = {}

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
    h: selfcord.Guild = client.get_guild(gid) # pyright: ignore
    thisUser: selfcord.Member = h.get_member(client.user.id)# pyright: ignore
    ch = h.channels # pyright: ignore
    cwin = windows["channels"]
    container = [None]*len(ch) # type: list[Window] # pyright: ignore
    channels = [None]*len(ch) # type: list[selfcord.abc.GuildChannel] #pyright: ignore
    for i in ch:
        if i.permissions_for(thisUser).view_channel == False: continue
        chIcon = ""
        match i.type.value:
            case 0: chIcon = "\uf4df"
            case 1: chIcon = "\uf456"
            case 2: chIcon = "\ue638"
            case 4: chIcon = "\U000f035d"
            case 5: chIcon = "\U000f00e6"
            case 10 | 11 | 12: chIcon = "\u251c"
            case 13: chIcon = "\U000f1749"
            case 15: chIcon = "\U000f028c"
        
        if "music" in i.name: chIcon = "\U000f02cb"
        container[i.position] = Window(FormattedTextControl(chIcon+" "+i.name),width=22,height=1)
        channels[i.position] = i # pyright: ignore
    channels = list(filter(lambda h: h is not None, channels))
    container = list(filter(lambda h: h is not None, container))

    cwin.content.children = container # pyright: ignore
    app._redraw()

async def create_msg_window(i: selfcord.Message):
    global lastUser
    if i.content != "":
        h=HSplit([
            Window(FormattedTextControl(PygmentsTokens(await help.format_message(client, i)),focusable=True),wrap_lines=True)
        ])
    else:
        h=HSplit([])
    for attach in i.attachments:
        h.children.append(Window(FormattedTextControl("\U000f0066 "+attach.url,tc.url)))
    if i.author.id != lastUser:
        usr = i.author
        if type(usr) == selfcord.Member:
            for r in usr.roles:
                if r.color.value != selfcord.Colour.from_str("#B9BBBE").value:
                    userColorsCache[i.author.id][i.channel.guild.id] = r.color.__str__()
                    break
        else:
            userColorsCache[(i.author.id)] = "#B9BBBE"
        h.children.insert(0, VSplit([
            Window(FormattedTextControl(i.author.display_name,"fg:"+"")),
            Window(FormattedTextControl(i.created_at.strftime("%m/%d/%Y, %H:%M:%S"),"fg:gray"))
        ],height=1))
    if (msgref:=i.reference) is not None:
        msg = msgref.resolved
        if type(msg) == selfcord.Message:
            h.children.insert(0, VSplit([
                Window(FormattedTextControl("\U000f0772"),width=1),
                Window(FormattedTextControl(msg.author.name+"  ",style="fg:"+msg.author.color.__str__()),width=len(msg.author.name)+2),
                Window(FormattedTextControl(msg.content),height=1,wrap_lines=False, style="fg:gray")
            ]))
        else:
            h.children.insert(0, VSplit([
                Window(FormattedTextControl("\U000f0772")),
                Window(FormattedTextControl("Cannot load the message." if type(msg) == None else "Original message was deleted.", style="italic fg:gray"))
            ]))
    if client.user in i.mentions:
        h.style = tc.msgMentionHighlight
    lastUser = i.author.id
    return h

async def render_messages(cid:int):
    global messages, windows, lastUser
    stfupyright: selfcord.TextChannel = await help.get_or_fetch(client, "channel", cid) # pyright: ignore
    messages = [i async for i in stfupyright.history(limit = 50)]
    container = []
    for i in messages:
        h = await create_msg_window(i)
        container.insert(0, h)
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

    @kb.add("enter", filter=Condition(lambda: mode != 1))
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
            await render_messages(chInfo.id)
            focusingCh = chInfo.id
            mode = 2
            scrollTarget="messageContent"
            scrollCursorPos["messageContent_"+str(focusingCh)] = len(windows["messageContent"].content.children)-1

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
        if mode == 1:
            mode = 2 
            app.layout.focus(windows["messageContent"].content.children[scrollCursorPos["messageContent_"+str(focusingCh)]])

    @kb.add("i", filter=Condition(lambda: mode != 1 and focusingCh != 0))
    def input(e):
        global mode
        app.layout.focus(inputBoxes["messageInput"])
        mode = 1

    @kb.add("c-q")
    async def shut(e: KeyPressEvent):
        e.app.exit()
        await client.close()

    return kb
 


async def main():
    global windows, client, app, inputBoxes
    conf = help.loadJson("config.json")
    windows = {
        "guilds": ScrollablePane(HSplit([Window()],style=tc.secondaryBg,width=12),show_scrollbar=False),
        "channels":ScrollablePane(HSplit([Window()],width=22,style=tc.channelListBg),show_scrollbar=False),
        "messageContent":ScrollablePane(HSplit([Window()],style=tc.mainBg), max_available_height=848940300),
        "typing":VSplit([],height=1, style=tc.secondaryBg),
        "VerticalLine": Window(char=" ", style="class:line,vertical-line "+tc.secondaryBg, width=1)
    }
    def t(**kwargs):
        buf = Buffer()
        return (Window(BufferControl(buf),**kwargs), buf)
    inputBoxes = {
        "messageInput": TextArea(height = 2, style = tc.mainBg,dont_extend_width=True),
    }
    windows["messages"] = HSplit([windows["messageContent"], inputBoxes["messageInput"]]) # pyright: ignore
    windows["typingList"] = Window(FormattedTextControl())
    
    win, buf = t(width=3, height=1, style=tc.secondaryBg)
    windows["typingAnim"] = win
    async def typingAnim():
        seq = [
            "\U000f09de\U000f0765\U000f0765",
            "\U000f0765\U000f09de\U000f0765",
            "\U000f0765\U000f0765\U000f09de",
            "\U000f0765\U000f0765\U000f0765"
        ]
        idx = 0
        while True:
            buf.cursor_position=0
            buf.text=seq[idx]
            await asyncio.sleep(0.5)
            idx += 1 
            if idx == 4: idx = 0
            if app.is_running == False: return

    kb = keybind_lore() 

    lay = Layout(HSplit([HSplit([Window(),Window(FormattedTextControl("\n\U000f066f"),align=WindowAlign.CENTER)]),Window(FormattedTextControl("Loading Disconsole"), height=2, align=WindowAlign.CENTER)],style=tc.mainBg))
    app = Application(lay,full_screen=True,mouse_support=True, key_bindings=kb,style=style_from_pygments_cls(help.DisconsoleStyle))
        
    import platform
    if platform.system() == "Windows":
        from ctypes import windll, pointer, c_ulong
        from ctypes.wintypes import DWORD, HANDLE

        h = DWORD()
        handle = HANDLE(windll.kernel32.GetStdHandle(c_ulong(-10)))
        windll.kernel32.GetConsoleMode(handle, pointer(h))
        windll.kernel32.SetConsoleMode(handle, h.value | 0x0001)
    client = selfcord.Client()


    @client.event 
    async def on_ready():
        mainw = VSplit([
            windows["guilds"],
            windows["VerticalLine"],
            HSplit([
                windows["channels"],
                HSplit([
                    Window(FormattedTextControl(client.user.display_name)),# pyright: ignore
                    Window(FormattedTextControl(client.user.name,style="fg:#6B6F77"))# pyright: ignore
                ], height=2, style=tc.secondaryBg)
            ]),
            windows["VerticalLine"],
            windows["messages"]
        ])
        asyncio.ensure_future(typingAnim(),loop=asyncio.get_event_loop())

        app.layout.container = mainw

        app.invalidate()

        render_guilds()

    @client.event
    async def on_message(i: selfcord.Message):
        global lastUser
        if focusingCh == i.channel.id:
            h = await create_msg_window(i)
            windows["messageContent"].content.children.append(h)
            lastUser = i.author.id

            app.layout.focus(h)

    @client.event 
    async def on_typing(ch: selfcord.TextChannel, usr: selfcord.Member, when: datetime):
        if ch.id == focusingCh:...

    @client.event
    async def on_error(*no, **noo):
        traceback.print_exc(file=open("tb","a"))
    with patch_stdout(): await asyncio.wait([asyncio.create_task(client.start(token=conf["token"])), asyncio.create_task(app.run_async())])# pyright: ignore

asyncio.run(main())
