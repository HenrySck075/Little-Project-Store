import curses, discord, json, random, math, threading
import patcho, help # patch pycord http to use bot token
from typing import TypedDict
from curses import textpad

cursesWindow = curses._CursesWindow
cursesTextbox= textpad.Textbox


class keyList(list):
    def __init__(self, iter):
        super().__init__(iter)
    def __getitem__(self, i):
        if i >= self.__len__(): return -2
        return list.__getitem__(self, i)
# session states
keys = keyList([])
mode = 0 # 0 for cmd, 1 for input
scrollTarget = ""
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

def kbListener(evWindow: cursesWindow):
    curses.halfdelay(35)
    while True:
        match evWindow.getch():
            case 105: # i
                updMode(1,"msgBar")
                break
            case 113: # q
                updMode(0)
            case 115: # s
                if len(keys) == 0: keys.append(115)
                elif keys[0] == 27: ... # search message
            case 103: # g 
                if keys[0] == 27:
                    # scrolling server list 
                    "a"
            case 27:
                keys.append(27)
            case curses.KEY_REFRESH:...


def border(win:cursesWindow,ls=curses.ACS_VLINE,rs=curses.ACS_VLINE,ts=curses.ACS_HLINE,bs=curses.ACS_HLINE,tl=curses.ACS_ULCORNER,tr=curses.ACS_URCORNER,bl=curses.ACS_LLCORNER,br=curses.ACS_LRCORNER,**padparams):
    win.border(ls,rs,ts,bs,tl,tr,bl,br)
    try: win.refresh(**padparams)
    except TypeError: win.refresh()

def main():
    global windows, colorable, client, textpads
    conf: dict = help.loadJson("config.json") # pyright: ignore
    windows: dict[str,cursesWindow] = {}
    textpads: dict[str,cursesTextbox] = {}
    messageWindows = []

    # init curses
    stdscr = curses.initscr()
    
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


    #setup connection
    client = discord.Client()

    @client.event 
    async def on_ready():
        windows["eventListener"] = curses.newwin(1,curses.COLS,curses.COLS-1,0)
        windows["guilds"] = stdscr.subpad(curses.LINES,7,0,0)
        windows["channels"] = stdscr.subpad(curses.LINES,12,0,7)
        windows["messages"] = stdscr.subpad(curses.LINES-1,curses.COLS-19,0,19)
        windows["msgBorder"] = stdscr.subpad(4,curses.COLS-21,curses.LINES-6,20)
        textpads["msgBar"] = textpad.Textbox(windows["msgBorder"].subwin(2,curses.COLS-19,curses.LINES-5,21))
        
        border(windows["channels"])
        windows["eventListener"].touchwin()
        windows["eventListener"].keypad(True)

    # connect
    client.run(conf["token"])


main()
