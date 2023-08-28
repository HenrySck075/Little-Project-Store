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

def patch(config: dict = {}, download_conf: dict = {}, search_conf: dict = {}, grab_conf: dict = {}):
    """
    Applied patches:
    ~~~
    | - `core`\n
    | - - -| - `cli`\n
    | - - -| - - -| - `helpers`\n
    | - - -| - - -| - - -| - - - `banner`: Removed pointless check\n
    | - - -| - - -| - - -| - - - `stream_handlers`: mute the logger when requested\n
    | - - -| - - -| - `commands`: Returns the data when called\n
    | - - -| - `codebase`\n
    | - - -| - - -| - `downloader`\n
    | - - -| - - -| - - -| - `handle`: Passing the progress callback for `core.cli.commands.download.animdl_download`\n
    | - - -| - - -| - `helpers`: fix regex\n
    | - `utils`\n
    | - - -| - `media_downloader`: Final destination for progress callback (see `core.codebase.downloader.handle` desc)
    
    """
    from .patches.core.cli.commands import download, search, grab
    from .patches.core.cli.helpers import banner, stream_handlers
    from .patches.core.codebase.downloader import handle as handle_patch
    from .patches.core.codebase import helpers as codebase_helpers_patch
    from .patches.utils import media_downloader
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
    media_downloader.patch()



