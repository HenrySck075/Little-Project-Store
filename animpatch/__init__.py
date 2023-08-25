from . import download
from enum import Enum

class Function(Enum):
    download = 1

def addMissing(d: dict):
    return {
        "keep_banner": False,
        "keep_cnd": False,
        "log": True
    } | d

def patch(config: dict, download_conf = {}):
    config = addMissing(config)
    def i(conf: dict, type: int):
        j = config | conf
        globals()[Function(type).name].patch(**j)

    i(download_conf, 1)


