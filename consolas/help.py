import json
from typing import TypeVar, Any, Union
import pygments

import selfcord
MessageableChannel = Union[selfcord.TextChannel, selfcord.VoiceChannel, selfcord.StageChannel, selfcord.Thread, selfcord.DMChannel, selfcord.PartialMessageable, selfcord.GroupChannel]
class MissingSentinel:
    def __repr__(self):
        return "..."
    def __str__(self) -> str:
        return self.__repr__()
MISSING = MissingSentinel()
# funky functions
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

async def get_or_fetch(obj, attr, id, default = MISSING, **kwargs) -> Any:
    call = getattr(obj,"get_"+attr)(id, **kwargs)
    if call is None:
        try:
            call = await getattr(obj, ("fetch_" if hasattr(obj,"fetch_"+attr) else "_fetch_")+attr)(id, **kwargs)
        except (selfcord.HTTPException, ValueError):
            if default != MISSING:return default
            else: raise
    return call
# Pygments
from pygments.lexer import RegexLexer
from pygments.style import Style
from pygments.formatter import Formatter
from pygments.token import _TokenType
DisconsoleToken = _TokenType().Disconsole
class ThemeColors:
    focusHighlight = "bg:#35373C"
    mainBg = "bg:#313338"
    channelListBg = "bg:#2B2D31"
    secondaryBg = "bg:#232428"
    selectHighlight = "bg:#404249"
    msgFocusHighlight = "bg:#2F3238"
    msgMentionHighlight = "bg:#444037"
    url = "fg:#00A8FC"
    mentionTextHighlight = "bg:#4e4e74"
tc = ThemeColors()

class DisconsoleLexer(RegexLexer):
    tokens = {
        "root": [
            (r'[a-zA-Z]*:\/\/(\S*)', DisconsoleToken.URL),
            (r'<#(\d*)>', DisconsoleToken.MentionChannel),
            (r'<@(\d*)>', DisconsoleToken.MentionUser)
        ]
    }

class DisconsoleStyle(Style):
    styles = {
        DisconsoleToken.URL: tc.url.replace("fg:",""),
        DisconsoleToken.MentionChannel: tc.mentionTextHighlight,
        DisconsoleToken.MentionUser: tc.mentionTextHighlight
    }


async def format_message(client: selfcord.Client, msg: selfcord.Message):
    h = []
    for ttype, v in pygments.lex(msg.content, DisconsoleLexer()):
        if ttype == DisconsoleToken.MentionChannel:
            v = "# " + (await get_or_fetch(client, "channel", int(v.replace("<#","").replace(">","")))).name
        if ttype == DisconsoleToken.MentionUser:
            id = int(v.replace("<@","").replace(">",""))
            usr: selfcord.User | selfcord.Member = await (get_or_fetch(client, "user", id) if type(msg.channel) == selfcord.DMChannel else get_or_fetch(msg.channel.guild, "member", id))
            v = "@ " + usr.display_name
        h.append((ttype,v))
    return h
