import curses, discord, json, random, math, threading
import patcho, help # patch pycord http to use bot token
from typing import TypedDict

cursesWindow = curses._CursesWindow
class Windows(TypedDict, total=False):
    channels: cursesWindow
    messages: cursesWindow
    guilds: cursesWindow
    msgBar: cursesWindow
    eventListener: cursesWindow

class dict4cw(dict):
    def __setitem__(self, __key: str, __value: cursesWindow) -> None:
        __value.borderStruct = {} # pyright: ignore
        __value.border()
        return super().__setitem__(__key, __value)

def listener(evWindow: cursesWindow):
    curses.halfdelay(35)
    while True:...

def focus(win: cursesWindow):
    try: win.borderStruct
    except AttributeError: return
    
    win.attron(curses.COLOR_YELLOW)
    win.border(**win.borderStruct)
    win.attroff(curses.COLOR_YELLOW)
    win.refresh()

def main():
    global windows, colorable
    conf: dict = dict4cw(help.loadJson("config.json")) # pyright: ignore
    windows: Windows = {}

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
        windows["guilds"] = curses.newwin(curses.LINES,7,0,0)
        windows["channels"] = curses.newwin(curses.LINES,12,0,7)


        windows["eventListener"].touchwin()

    # connect
    client.run(conf["token"])


main()
