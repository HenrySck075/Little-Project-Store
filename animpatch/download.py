import logging
from pathlib import Path

import click
from rich.text import Text

from animdl.core.__version__ import __core__
from animdl.core.codebase import providers, sanitize_filename
from animdl.core.config import (
    AUTO_RETRY,
    CHECK_FOR_UPDATES,
    DEFAULT_PROVIDER,
    DOWNLOAD_DIRECTORY,
    QUALITY,
)
from animdl.core.cli import exit_codes, helpers, http_client

import animdl.core.cli.commands.download

from animpatch.exc import DownloaderException, ExtractionError, NoContentFound, prinnt
from .helpers import MessageType, dic, send_exc

@helpers.decorators.content_fetch_options(
    default_quality_string=QUALITY,
)
@helpers.decorators.download_options(
    default_download_dir=DOWNLOAD_DIRECTORY,
)
def animdl_download(
    query, special, quality, download_dir, idm, index, log_level, **kwargs
):
    r = kwargs.get("range")

    console = helpers.stream_handlers.get_console()

    anime, provider = helpers.process_query(http_client.client, query, console, auto_index=index, provider=DEFAULT_PROVIDER)

    if not anime:
        yield send_exc(NoContentFound("Could not find an anime of that name :/."))

    match, provider_module, _ = providers.get_provider(
        providers.append_protocol(anime.get("anime_url"))
    )

    yield dic(
        type=1,
        subtype=1,
        data=dic(
            provider=provider,
            anime_url = anime['anime_url']
        )
    )
    streams = list(
        provider_module.fetcher(
            http_client.client, anime.get("anime_url"), r, match
        )
    )

    if special:
        streams = list(helpers.special.special_parser(streams, special))

    download_directory = Path(download_dir).resolve(strict=True)
    content_name = sanitize_filename(anime["name"])

    content_dir = download_directory / content_name

    yield dic(
        type=1,
        subtype=2,
        data = dic(
            directory = content_dir.resolve().as_posix()
        )
    )
    total = len(streams)

    if total < 1:
        console.print(Text("Could not find any streams on the site :/."))
        console.print(
            "This could mean that, either those episodes are unavailable or that the scraper has broke.",
            style="dim",
        )

    with helpers.stream_handlers.context_raiser(
        console, f"Now downloading {content_name!r}", name="downloading"
    ):
        for count, (stream_urls_caller, episode_number) in enumerate(streams, 1):
            stream_urls = helpers.ensure_extraction(
                http_client.client, stream_urls_caller
            )

            content_title = f"E{int(episode_number):02d}"

            if not stream_urls:
                prinnt(NoContentFound(
                    f"Could not find any streams for {content_title!r} :/.",
                    )
                )
                continue

            console.print(
                f"Currently downloading: {content_title!r}. [dim]{total-count:d} episodes in queue.[/]",
            )

            expected_download_path = content_dir / content_title

            status_enum, exception = helpers.safe_download_callback(
                session=http_client.client,
                logger=logger,
                stream_urls=stream_urls,
                quality=quality,
                expected_download_path=expected_download_path,
                use_internet_download_manager=idm,
                retry_timeout=AUTO_RETRY,
                log_level=log_level,
            )
            # use match bruh
            if status_enum == helpers.SafeCaseEnum.NO_CONTENT_FOUND:
                prinnt(NoContentFound(
                    f"Could not find any streams for {content_title!r}",
                ))
                continue

            if status_enum == helpers.SafeCaseEnum.EXTRACTION_ERROR:
                prinnt(ExtractionError(
                    f"Could not extract any streams for {content_title!r} due to: {exception!r}",
                ))
                continue

            if status_enum == helpers.SafeCaseEnum.DOWNLOADER_EXCEPTION:
                prinnt(DownloaderException(
                    f"Internal downloader error occured for {content_title!r}.",
                ))
                continue

def patch(keep_cmd: bool = False, keep_banner: bool = False):
    f = animdl_download
    if keep_banner: f = (helpers.decorators.banner_gift_wrapper(http_client.client, __core__, check_for_updates=CHECK_FOR_UPDATES))(f)
    if keep_cmd: f = click.command(name="download", help="Download your favorite anime by query.")(helpers.decorators.automatic_selection_options()(f))
    animdl.core.cli.commands.download.animdl_download = f
