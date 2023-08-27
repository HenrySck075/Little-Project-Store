import functools
from rich.console import Console

class NotConsole:
    def __init__(self, **kwargs) -> None:
        pass

    def print(self, **kwargs): pass

def get_console(log=True):
    return Console(stderr=True, color_system="auto") if log else NotConsole()

def patch():
    import animdl.core.cli.helpers.stream_handlers as sh_patch
    sh_patch.get_console = functools.lru_cache()(get_console)
