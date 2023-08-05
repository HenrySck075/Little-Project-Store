from prompt_toolkit import PromptSession
from prompt_toolkit.styles import style_from_pygments_cls, Style
from prompt_toolkit.lexers import PygmentsLexer
from pygments.styles.colorful import ColorfulStyle
from pygments.lexers.python import Python3Lexer, Python3TracebackLexer
from pygments.formatters import HtmlFormatter
from pygments import highlight
import traceback
import sys
fakeglobals={}
session = PromptSession()

def prompt_continuation(width, _, __):
    return '.' * (width-1) + " "
    # Or: return [('', '.' * width)]
print(f"Python {sys.version} on {sys.platform}")
print('Type "help", "copyright", "credits" or "license" for more information.\nPress Meta+Enter (or Esc+Enter) to move to new line.')
while True:
    cmd = session.prompt(">>> ",multiline=True,style=style_from_pygments_cls(ColorfulStyle),lexer=PygmentsLexer(Python3Lexer),prompt_continuation=prompt_continuation)
    try:
        exec(cmd,fakeglobals)
    except Exception as e:
        highlight(traceback.format_exc(),Python3TracebackLexer(),HtmlFormatter())