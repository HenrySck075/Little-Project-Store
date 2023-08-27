import httpx, logging, pathlib
from typing import Optional, Dict
from pathlib import Path
from tqdm import tqdm
from animdl.core.config import THREADED_DOWNLOAD
from animdl.core.codebase.downloader.handle import subautomatic, hls_download, idm_download, FFMPEG_HLS, POSSIBLE_VIDEO_EXTENSIONS, DEFAULT_MEDIA_EXTENSION, EXEMPT_EXTENSIONS
from animdl.core.codebase.downloader.ffmpeg import FFMPEG_EXTENSIONS, ffmpeg_download, has_ffmpeg
from animdl.core.codebase.downloader.hls import HLS_STREAM_EXTENSIONS

from ....helpers import PROGRESS_CALLBACK

import animdl.utils.media_downloader as media_downloader
import animdl.utils.serverfiles as serverfiles


@subautomatic
def handle_download(
    session: httpx.Client,
    url: str,
    expected_download_path: pathlib.Path,
    use_internet_download_manager=False,
    headers: Optional[Dict[str, str]] = None,
    **opts,
):
    download_handling_logger = logging.getLogger("animdl/download-handler")

    prefetch_response = media_downloader.prefetch(
        session, opts.get("method", "GET"), url, headers=headers
    )

    content_disposition = prefetch_response.headers.get("Content-Disposition")

    server_filename = None

    if server_filename is None and content_disposition:
        server_filename = serverfiles.guess_from_content_disposition(
            content_disposition
        )

    content_type = prefetch_response.headers.get("Content-Type")

    if server_filename is None and content_type:
        server_filename = serverfiles.guess_from_content_type("file", content_type)

    if server_filename is None:
        server_filename = serverfiles.guess_from_path(prefetch_response.url.path)

    content_range = prefetch_response.headers.get("Content-Range")

    if content_range is not None:
        content_size = int(content_range.split("/", 1)[1])
    else:
        content_size = None

    ranges = prefetch_response.status_code == 206 or (
        prefetch_response.headers.get("Accept-Ranges") == "bytes"
    )

    if server_filename and "." in server_filename:
        _, extension = server_filename.rsplit(".", 1)
    else:
        extension = None

    if extension not in POSSIBLE_VIDEO_EXTENSIONS:
        download_handling_logger.warn(
            f"The server gave filename as {server_filename!r} but the project is unsure whether this format is what it intends to use. "
            f"Hence, the downloader will be using {DEFAULT_MEDIA_EXTENSION!r}, the file format may be different or the file may end up as corrupted"
            ", in those cases, do report at project's issue tracker."
        )
        extension = DEFAULT_MEDIA_EXTENSION

    expected_download_path = expected_download_path.with_suffix(f".{extension}")

    download_handling_logger.info(
        f"Server filename: {server_filename!r}, project inferred: {expected_download_path.name!r}",
    )

    expected_download_path.parent.mkdir(parents=True, exist_ok=True)

    if FFMPEG_HLS and (extension in FFMPEG_EXTENSIONS and has_ffmpeg()):
        return_code = ffmpeg_download(url, headers, expected_download_path, **opts)

        if return_code:
            raise Exception(
                f"ffmpeg exited with non-zero return code {return_code}, download failed."
            )

        return expected_download_path.with_suffix(".mkv")

    if extension in EXEMPT_EXTENSIONS:
        raise Exception(
            "Download extension {!r} requires custom downloading which is not supported yet.".format(
                extension
            )
        )

    if extension in HLS_STREAM_EXTENSIONS:
        return hls_download(session, url, expected_download_path, headers or {}, **opts)

    if use_internet_download_manager:
        return idm_download(url, headers or {}, expected_download_path, **opts)

    return standard_download(
        session,
        url,
        expected_download_path,
        content_size,
        headers,
        ranges,
        log_level=opts.get("log_level", 20),
        retry_timeout=opts.get("retry_timeout", 5.0),
        callback=opts.get("callback", PROGRESS_CALLBACK)
    )

def standard_download(
    session: httpx.Client,
    url: str,
    expected_download_path: Path,
    content_size: "Optional[int]" = None,
    headers: "Optional[dict]" = None,
    ranges: bool = True,
    log_level: int = 20,
    retry_timeout: float = 5.0,
    method="GET",
    callback=PROGRESS_CALLBACK
):
    expected_download_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(f"downloader/standard[{expected_download_path.name}]")

    with open(expected_download_path, "ab") as download_io:
        position = download_io.tell()

        if position:
            if not ranges:
                logger.critical(
                    "Stream does not support ranged downloading, the previous download cannot be continued."
                )
                download_io.seek(0)
                position = 0

            if THREADED_DOWNLOAD:
                logger.critical(
                    "Download will not be continued as continuation is not supported in threaded downloads."
                )
                download_io.seek(0)
                position = 0

        progress_bar = tqdm(
            desc=f"{method} / {expected_download_path.name}",
            total=content_size,
            disable=True,
            initial=position,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        downloader = media_downloader.MultiConnectionDownloader(
            session,
            method,
            url,
            headers=headers,
            retry_timeout=retry_timeout,
            progress_bar=progress_bar,
            callback=callback
        )

        downloader.allocate_downloads(
            download_io, # type: FileIO
            content_size,
            start_at=position,
            threaded=ranges and THREADED_DOWNLOAD,
        )

    progress_bar.close()
    return expected_download_path

def patch():
    import animdl.core.codebase.downloader.handle
    from ....utils import media_downloader as md_patch
    md_patch.patch()
    animdl.core.codebase.downloader.handle.standard_download = standard_download
    animdl.core.codebase.downloader.handle.handle_download = handle_download
