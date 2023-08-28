from . import banner, stream_handlers


from ....helpers import PROGRESS_CALLBACK
import logging
import traceback
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, Generator, Optional
    import pathlib

    import httpx

from animdl.core.cli.helpers import intelliq, further_extraction
import animdl.core.cli.helpers
from animdl.core.codebase import downloader
from ....exc import *

def safe_download_callback(
    session: "httpx.Client",
    logger: "logging.Logger",
    stream_urls: "Generator[Dict[str, Any], None, None]",
    quality: str,
    expected_download_path: "pathlib.Path",
    use_internet_download_manager: bool = False,
    retry_timeout: "Optional[int]" = None,
    log_level: "Optional[int]" = None,
    progress_callback = PROGRESS_CALLBACK,
    **kwargs,
) -> "pathlib.Path":
    flattened_streams = list(stream_urls)

    try:
        streams = intelliq.filter_quality(flattened_streams, quality)
    except Exception as exception:
        raise ExtractionError(" ".join(exception.args))

    if not streams:
        raise NoContentFound("No streams found")

    for stream in streams:
        needs_further_extraction = "further_extraction" in stream

        if needs_further_extraction:
            try:
                safe_download_callback(
                    session,
                    logger,
                    further_extraction(session, stream),
                    quality,
                    expected_download_path,
                    use_internet_download_manager,
                    retry_timeout,
                    log_level,
                    **kwargs,
                )

            except NoContentFound:
                logger.debug("Could not find streams on further extraction, skipping.")
                continue

            except ExtractionError as e:
                logger.error(
                    f"Could not extract streams from further extraction due to an error: {' '.join(e.args)}, skipping."
                )
                continue

            except DownloaderException:
                logger.error(
                    f"Could not download streams from further extraction due to multiple errors, skipping."
                )
                continue

        else:
            try:
                path = downloader.handle_download(
                    session=session,
                    url=stream["stream_url"],
                    expected_download_path=expected_download_path,
                    use_internet_download_manager=use_internet_download_manager,
                    headers=stream.get("headers"),
                    preferred_quality=quality,
                    subtitles=stream.get("subtitle"),
                    callback=progress_callback,
                    **kwargs,
                )
                return path

            except Exception as download_exception:
                logger.error(
                    f"Could not download stream due to an error: {download_exception!r}, skipping."
                )
                logger.debug(f"Traceback for the above error: {traceback.format_exc()}")

        logger.critical(
            "Could not download any streams. Use the project with 0 log level to view errors for debugging and bug reporting purposes."
        )

        raise NoContentFound("Could not download any streams. Use the project with 0 log level to view errors for debugging and bug reporting purposes.")

def patch():
    from ...codebase import downloader as downloader_patch
    downloader_patch.handle.patch()

    animdl.core.cli.helpers.safe_download_callback = safe_download_callback
