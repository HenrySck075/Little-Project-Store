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

raiseExceptions = True

class DisabledLogger(Logger):
    "No matter what you're trying to do, it won't print"
    def __init__(self, name: str, level: _Level = 0) -> None:
        super().__init__(name, level)
    
    def log(self, level, msg, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """
        pass

# constants
PROGRESS_CALLBACK = lambda progress, total: ""
