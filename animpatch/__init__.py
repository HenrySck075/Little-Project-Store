from enum import Enum

class Function(Enum):
    download = 1
    search = 2

def addMissing(d: dict):
    return {
        "keep_banner": False,
        "log": True
    } | d

def patch(config: dict, download_conf = {}, search_conf = {}):
    from .core.cli.commands import download, search
    from .core.cli.helpers import banner, stream_handlers
    from .core.codebase.downloader import handle as handle_patch
    banner.patch()
    stream_handlers.patch()
    config = addMissing(config)
    def i(conf: dict, type: int):
        j = config | conf
        globals()[Function(type).name].patch(**j)

    i(download_conf, 1)
    i(search_conf, 2)
    handle_patch.patch()



