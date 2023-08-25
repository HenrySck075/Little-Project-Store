from io import FileIO
from typing import Optional, Dict
import threading, httpx
from tqdm import tqdm
from ..core.cli.helpers.constants import PROGRESS_CALLBACK
def init(
    self,
    session: httpx.Client,
    *args,
    progress_bar: "Optional[tqdm]" = None,
    retry_timeout: "Optional[int]" = None,
    **kwargs,
):
    self.session = session
    self.progress_bar = progress_bar
    self.retry_timeout = retry_timeout

    self.args = args
    self.kwargs = kwargs

    self.io_lock = threading.Lock()
    self.active_threads: "Dict[str, threading.Thread]" = {}
    self.threads_errors: "Dict[str, Exception]" = {}

    self.callback = kwargs.get("callback",PROGRESS_CALLBACK)

def download_section(
    self,
    io: "FileIO",
    start: int,
    end: int,
    progress_bar: "Optional[tqdm]" = None,
    pause_event: "Optional[threading.Event]" = None,
    error_event: "Optional[threading.Event]" = None
):
    kwargs = self.kwargs.copy()

    headers = kwargs.pop("headers") or {}
    content_length = end
    position = start or 0

    is_incomplete = lambda: content_length is None or position < content_length
    is_downloading = lambda: (error_event is None or not error_event.is_set()) and (
        pause_event is None or not pause_event.is_set()
    )

    retry_count = 0

    while is_downloading() and is_incomplete():
        if content_length is None:
            if start is not None:
                headers["Range"] = f"bytes={position}-"
        else:
            headers["Range"] = f"bytes={position}-{content_length}"

        try:
            with self.session.stream(
                *self.args, **kwargs, headers=headers
            ) as response:
                content_length:int|None = (
                    int(response.headers.get("Content-Length", 0)) or None
                )

                if progress_bar is not None:
                    if content_length > 0:
                        progress_bar.total = content_length

                for chunk in response.iter_bytes(8192):
                    chunk_size = len(chunk)

                    if self.progress_bar is not None:
                        self.progress_bar.update(chunk_size)

                    if progress_bar is not None:
                        progress_bar.update(chunk_size)

                    self.write_to_file(
                        self.io_lock,
                        io,
                        position,
                        chunk,
                    )
                    position += chunk_size

                    if not is_downloading():
                        break

                if content_length is None:
                    content_length = position

        except httpx.HTTPError as error:
            if retry_count >= self.MAX_RETRIES:
                locks = ()

                if progress_bar is not None:
                    locks += (progress_bar.get_lock(),)
                if self.progress_bar is not None:
                    locks += (self.progress_bar.get_lock(),)

                self.threads_errors[threading.current_thread().name] = error

                if error_event is not None:
                    error_event.set()
            else:
                if self.retry_timeout is not None:
                    time.sleep(self.retry_timeout)

                retry_count += 1

    return (start, position)

def patch():
    import animdl.utils.media_downloader as media_downloader
    media_downloader.MultiConnectionDownloader.__init__ = init
    media_downloader.MultiConnectionDownloader.download_section = download_section
