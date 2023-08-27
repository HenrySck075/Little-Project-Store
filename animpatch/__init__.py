from .core.cli.commands import download
from .core.cli.helpers import banner
from enum import Enum

class Function(Enum):
    download = 1

def addMissing(d: dict):
    return {
        "keep_banner": False,
        "log": True
    } | d

def patch(config: dict, download_conf = {}):
    banner.patch()
    config = addMissing(config)
    from .core.codebase.downloader import handle as handle_patch
    def i(conf: dict, type: int):
        j = config | conf
        globals()[Function(type).name].patch(**j)

    i(download_conf, 1)
    handle_patch.patch()



