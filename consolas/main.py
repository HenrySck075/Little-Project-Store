import help, keys as ordkeys # patch pycord http to use bot token
exec(open("patcho.py","r").read(),globals())
import curses, discord, json, random, math, threading
from typing import TypeVar, Generic
from curses import textpad
import asyncio
from rich.traceback import install
install(show_locals=True)
cursesWindow = curses.window
cursesTextbox= textpad.Textbox

def keygen(module):
    return {("Shift > " + name.replace("_UP","") if "_UP" in name and name != "KEY_UP" else name):module.__dict__[name] for name in module.__dict__.keys() if "KEY_" in name}


class keyList(list):
    def __init__(self, iter):
        super().__init__(iter)
    def __getitem__(self, i):
        if i >= self.__len__(): return -2
        return list.__getitem__(self, i)
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
        return super().__setitem__(__key, __value)
# session states
keys = keyList([])
mode = 0 # 0 for cmd, 1 for input
scrollTarget = ""
scrollCursorPos = DefaultDict[str,tuple[int,int]]({},(0,0))
focusingG = 0
focusingCh = 0
guilds = []
channels = []
messages = []


def fieldsValidator(i):
    global keys
    if i == 27:
        keys.append(27)
    elif i == 10 or i == curses.KEY_ENTER:
        if not (len(keys) == 1 and keys[0] == 27):
            return 7
    else: keys = []
    return i

def updMode(m,target:str=""):
    global mode
    match m:
        case 0:
            windows["eventListener"].touchwin()
        case 1:
            if target == "msgBar":
                textpads["msgBar"].edit(fieldsValidator)

    mode = m
class ScrlCtrl:
    def up(self,n):
        n[0]-=1 
        return n
    def down(self,n):
        n[0]+=1 
        return n
    def left(self,n):
        n[1]-=1 
        return n
    def right(self,n):
        n[1]+=1 
        return n
scrlctrl = ScrlCtrl()

def render_guilds(x=0):
    global guilds, windows
    guilds = [(i.name, i.id) for i in client.guilds]
    gwin = windows["guilds"] 
    gwin.erase()
    ty = 0
    for i in guilds:
        gwin.addnstr(ty,0,i[0],6)
        ty+=1
    gwin.refresh(0,0,x,0,curses.LINES-1+x,6)

def render_channels(gid:int, x=0):
    global channels, windows
    channels = [(i.type, i.name,i.id) for i in asyncio.run(client.fetch_guild(gid)).channels]
    cwin = windows["channels"]
    cwin.erase()
    ty = 0
    for i in channels:
        chIcon = ""
        match i[0]:
            case 0: chIcon = "\uf4df"
            case 1: chIcon = "\uf456"
            case 2: chIcon = "\ue638"
            case 4: chIcon = "\U000f035d"
            case 5: chIcon = "\U000f00e6"
            case 10 | 11 | 12: chIcon = "\u251c"
            case 13: chIcon = "\U000f1749"
            case 15: chIcon = "\U000f028c"
        
        if "music" in i[1]: chIcon = "\U000f02cb"

        cwin.addnstr(ty,1,chIcon+" "+i[1],10)
        ty+=1 
    cwin.refresh(0,8,x,0,curses.LINES-5,curses.COLS-19)

def kbListener(evWindow: cursesWindow):
    global scrollTarget, scrollCursorPos
    curses.halfdelay(45)
    while True:
        match evWindow.getch():
            case ordkeys.KEY_I:
                updMode(1,"msgBar")
                break
            case ordkeys.KEY_Q:
                updMode(0)
            case ordkeys.KEY_S:
                if len(keys) == 0: keys.append(115)
                elif keys[0] == 27: ... # search message
            case ordkeys.KEY_G: # g 
                if keys[0] == 115:
                    # scrolling server list 
                    scrollTarget="guilds"
            case 27: #esc
                updMode(0)
            case curses.KEY_ENTER | 13: #enter key (13 is carriage return)
                if scrollTarget == "guilds":
                    render_channels(guilds[scrollCursorPos["guilds"][1]][1])
                    scrollTarget = "channels"
            case curses.KEY_REFRESH:
                windows["messages"].resize(curses.LINES-1,curses.COLS-19)
                

            # scrolling
            case curses.KEY_UP:
                scrollCursorPos = help.modifyValue(scrollCursorPos,scrollTarget, scrlctrl.up)
            case curses.KEY_DOWN:
                scrollCursorPos = help.modifyValue(scrollCursorPos,scrollTarget, scrlctrl.down)
            case curses.KEY_UP | curses.KEY_DOWN | curses.KEY_LEFT | curses.KEY_RIGHT:
                windows[scrollTarget].move(*scrollCursorPos[scrollTarget])

conf: dict = help.loadJson("config.json") # pyright: ignore
windows: dict[str,cursesWindow] = {}
textpads: dict[str,cursesTextbox] = {}
def main(stdscr):
    global windows, colorable, client, textpads, keynames
    messageWindows = []

    # init curses
    
    curses.noecho()
    curses.cbreak(False)
    colorable = curses.has_colors() and curses.can_change_color()
    if colorable:
        curses.start_color()

    centerX = int(curses.COLS / 2)

    # splash screen
    fact = help.sliceEvery(random.choice(help.loadJson("pasta.json")),int(curses.COLS*0.9))
    
    factYPos = int(curses.LINES / 2) - math.floor(len(fact) / 2)
    
    stdscr.addstr(factYPos - 2, centerX - 4, "Did you know....")

    for idx, i in enumerate(fact):
        stdscr.addstr(factYPos+idx,centerX-math.floor(len(i)/2),i)

    stdscr.addstr(curses.LINES - 2, centerX-9, "Loading Disconsole")

    stdscr.refresh()

    keynames = keygen(ordkeys) | keygen(curses)
    #setup connection
    client = discord.Client()

    @client.event 
    async def on_ready():
        windows["eventListener"] = curses.newwin(1,curses.COLS,curses.COLS-1,0)
        windows["guilds"] = stdscr.subpad(curses.LINES,6,0,0)
        windows["channels"] = stdscr.subpad(curses.LINES,10,0,8)
        windows["messages"] = stdscr.subpad(curses.LINES-5,curses.COLS-21,0,20)
        windows["msgBorder"] = stdscr.subpad(4,curses.COLS-21,curses.LINES-6,20)
        textpads["msgBar"] = textpad.Textbox(windows["msgBorder"].subwin(2,curses.COLS-19,curses.LINES-5,21))
        help.runmethod(list(windows.values())[1:],["scrollok(True)","idlok(True)"])

        stdscr.vline(0,7,"|",curses.LINES)
        stdscr.vline(0,19,"|",curses.LINES)
        windows["eventListener"].touchwin()
        windows["eventListener"].keypad(True)

    # connect
    client.run(conf["token"])


curses.wrapper(main)
