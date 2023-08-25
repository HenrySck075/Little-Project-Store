import httpx, logging
from typing import Optional
from pathlib import Path
from tqdm import tqdm
from animdl.core.config import THREADED_DOWNLOAD

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
            disable=log_level > 20,
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
        )

        downloader.allocate_downloads(
            download_io,
            content_size,
            start_at=position,
            threaded=ranges and THREADED_DOWNLOAD,
        )

    progress_bar.close()
    return expected_download_path

def patch():
    import animdl.core.codebase.downloader.handle
    animdl.core.codebase.downloader.handle.standard_download = standard_download
