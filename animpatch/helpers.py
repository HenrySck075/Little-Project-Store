from enum import Enum
from logging import _Level, Logger
class MessageType(Enum):
    error = -1
    info = 1
    progress = 2

class InfoSubtype(Enum):
    providers = 1
    download_location = 2
    dl_info = 3

def dic(**a): return a

def send_exc(msg): return dic(type=-1, excMessage=msg)

from functools import partial
def addKwargs(**the):
    def i(f):
        return partial(f, **the)
    return i

raiseExceptions = True

class DisabledLogger(Logger):
    "No matter what you're trying to do, it won't print"
    def __init__(self, name: str, level: _Level = 0) -> None:
        super().__init__(name, level)
    
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False,stacklevel=1):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.

        (It doesn't)
        """
        pass

# constants
PROGRESS_CALLBACK = lambda progress, total: ""
