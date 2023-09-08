import json
from typing import TypeVar


def loadJson(filename) -> dict | list: 
    return json.load(open(filename, "r"))

def addattr(o,**h):
    for i in h.keys():
        setattr(o,i,h[i])
    return o

def runmethod(iter:list, methods:list):
    for i in iter:
        h = {"i":i}
        [exec(f"i.{m}",h) for m in methods]

h = TypeVar("h", covariant=True, bound=dict)

def modifyValue(dic:h, key, stuff) -> h:
    if key != "":
        dic[key] = stuff(dic[key])
    return dic


from pygments.lexer import RegexLexer
from pygments.style import Style
from pygments.formatter import Formatter
from pygments.token import _TokenType
DisconsoleToken = _TokenType().Disconsole

class DisconsoleLexer(RegexLexer):
    tokens = {
        "root": [
            (r'[a-zA-Z]*:\/\/(\S*)', DisconsoleToken.URL)
        ]
    }

class DisconsoleStyle(Style):
    styles = {
        DisconsoleToken.URL: 'bg:#00A8FC'
    }

class DisconsoleFormatter(Formatter):
    def __init__(self, **opt):
        super().__init__(**opt)