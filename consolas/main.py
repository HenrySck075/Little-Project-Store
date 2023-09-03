import curses, discord, json
import patcho, help # patch pycord http to use bot token



def main():
    conf = help.loadJson("config.json")

