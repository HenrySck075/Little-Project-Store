from . import banner
import logging
import traceback
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from typing import Any, Dict, Generator, Optional, Tuple
    import pathlib

    import httpx

from animdl.core.cli.helpers import intelliq, further_extraction, SafeCaseEnum
import animdl.core.cli.helpers
from animdl.core.codebase import downloader

def safe_download_callback(
    session: "httpx.Client",
    logger: "logging.Logger",
    stream_urls: "Generator[Dict[str, Any], None, None]",
    quality: str,
    expected_download_path: "pathlib.Path",
    use_internet_download_manager: bool = False,
    retry_timeout: "Optional[int]" = None,
    log_level: "Optional[int]" = None,
    progress_callback: "Callable[[int, int], Any]",
    **kwargs,
) -> "Tuple[SafeCaseEnum, Optional[BaseException]]":
    flattened_streams = list(stream_urls)

    try:
        streams = intelliq.filter_quality(flattened_streams, quality)
    except Exception as exception:
        return SafeCaseEnum.EXTRACTION_ERROR, exception

    if not streams:
        return SafeCaseEnum.NO_CONTENT_FOUND, None

    for stream in streams:
        needs_further_extraction = "further_extraction" in stream

        if needs_further_extraction:
            status, potential_error = safe_download_callback(
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

            if status == SafeCaseEnum.DOWNLOADED:
                return status, potential_error

            if status == SafeCaseEnum.NO_CONTENT_FOUND:
                logger.debug(f"Could not find streams on further extraction, skipping.")
                continue

            if status == SafeCaseEnum.EXTRACTION_ERROR:
                logger.error(
                    f"Could not extract streams from further extraction due to an error: {potential_error}, skipping."
                )
                continue

            if status == SafeCaseEnum.DOWNLOADER_EXCEPTION:
                logger.error(
                    f"Could not download streams from further extraction due to multiple errors, skipping."
                )
                continue

        else:
            try:
                downloader.handle_download(
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
                return SafeCaseEnum.DOWNLOADED, None

            except Exception as download_exception:
                logger.error(
                    f"Could not download stream due to an error: {download_exception!r}, skipping."
                )
                logger.debug(f"Traceback for the above error: {traceback.format_exc()}")

        logger.critical(
            "Could not download any streams. Use the project with 0 log level to view errors for debugging and bug reporting purposes."
        )

        return SafeCaseEnum.NO_CONTENT_FOUND, None

def patch():
    from ...codebase import downloader as downloader_patch
    downloader_patch.handle.patch()

    animdl.core.cli.helpers.safe_download_callback = safe_download_callback
