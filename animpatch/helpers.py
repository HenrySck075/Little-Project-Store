from enum import Enum

class MessageType(Enum):
    error = -1
    info = 1
    progress = 2

class InfoSubtype(Enum):
    providers = 1
    download_location = 2

def dic(**a): return a

def send_exc(msg): return dic(type=-1, excMessage=msg)
