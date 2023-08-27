from enum import Enum

class Function(Enum):
    download = 1
    search = 2
    grab = 3

def addMissing(d: dict):
    return {
        "keep_banner": False,
        "log": True
    } | d

def patch(config: dict = {}, download_conf = {}, search_conf = {}, grab_conf = {}):
    """
    Applied patches:
    ~~~~~~~~~~~~~~~~
    | - `core`\n
    | - - -| - `cli`\n
    | - - -| - - -| - `helpers`\n
    | - - -| - - -| - - -| - - - `banner`: Add my name :)\n
    | - - -| - - -| - - -| - - - `stream_handlers`: mute the logger when requested\n
    | - - -| - - -| - `commands`: Returns the data when called\n
    | - - -| - `codebase`\n
    | - - -| - - -| - `downloader`\n
    | - - -| - - -| - - -| - `handle`: Passing the progress callback for `animdl.core.cli.commands.download.animdl_download`\n
    | - - -| - - -| - `helpers`: fix regex
    
    """
    from .core.cli.commands import download, search, grab
    from .core.cli.helpers import banner, stream_handlers
    from .core.codebase.downloader import handle as handle_patch
    from .core.codebase import helpers as codebase_helpers_patch
    banner.patch()
    stream_handlers.patch()
    config = addMissing(config)
    def i(conf: dict, type: int):
        nonlocal download, search, grab
        j = config | conf
        locals()[Function(type).name].patch(**j)

    i(download_conf, 1)
    i(search_conf, 2)
    i(grab_conf, 2)
    handle_patch.patch()
    codebase_helpers_patch.patch()



