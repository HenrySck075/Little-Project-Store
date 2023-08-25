from pathlib import Path

from typing import Generator, Dict, Optional, Any, Tuple

import logging
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
import animdl.core.cli.helpers as helpers, animdl.core.cli.http_client as http_client

import animdl.core.cli.commands.download

from ....exc import DownloaderException, ExtractionError, NoContentFound, prinnt
import ...codebase.downloader.handle as handle_patch
from .helpers import dic, send_exc


def animdl_download(
    query, special, quality, download_dir, idm, index, log_level, **kwargs
) -> Generator[Dict[str, int], None, None]:
    r = kwargs.get("range")

    console = helpers.stream_handlers.get_console()

    logger = logging.getLogger("downloader")

    anime, provider = helpers.process_query(
        http_client.client, query, console, auto_index=index, provider=DEFAULT_PROVIDER
    )

    if not anime:
        console.print(Text("Could not find an anime of that name :/."))
        raise SystemExit(exit_codes.NO_CONTENT_FOUND)

    logger.name = "{}/{}".format(provider, logger.name)

    match, provider_module, _ = providers.get_provider(
        providers.append_protocol(anime.get("anime_url"))
    )

    animes = []

    with helpers.stream_handlers.context_raiser(
        console,
        Text(
            f"Scraping juicy streams from {provider!r}@{anime['anime_url']}",
            style="bold magenta",
        ),
        name="scraping",
    ):
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

        animes[content_name] = {"directory": content_dir, "episodes": []}

        console.print(
            "The project will download to:",
            Text(content_dir.resolve().as_posix(), style="bold"),
        )
        total = len(streams)

        if total < 1:
            console.print(Text("Could not find any streams on the site :/."))
            console.print(
                "This could mean that, either those episodes are unavailable or that the scraper has broke.",
                style="dim",
            )
            raise SystemExit(exit_codes.NO_CONTENT_FOUND)

        with helpers.stream_handlers.context_raiser(
            console, f"Now downloading {content_name!r}", name="downloading"
        ):
            for count, (stream_urls_caller, episode_number) in enumerate(streams, 1):
                stream_urls = helpers.ensure_extraction(
                    http_client.client, stream_urls_caller
                )

                content_title = f"E{int(episode_number):02d}"

                if not stream_urls:
                    console.print(
                        Text(
                            f"Could not find any streams for {content_title!r} :/.",
                        )
                    )
                    continue

                console.print(
                    f"Currently downloading: {content_title!r}. [dim]{total-count:d} episodes in queue.[/]",
                )

                expected_download_path = content_dir / content_title

                status_enum, exception = helpers.safe_download_callback( # patch this to not log the progress created by tqdm
                    session=http_client.client,
                    logger=logger,
                    stream_urls=stream_urls,
                    quality=quality,
                    expected_download_path=expected_download_path,
                    use_internet_download_manager=idm,
                    retry_timeout=AUTO_RETRY,
                    log_level=log_level,
                )

                if status_enum == helpers.SafeCaseEnum.NO_CONTENT_FOUND:
                    console.print(
                        f"Could not find any streams for {content_title!r}",
                    )
                    continue

                if status_enum == helpers.SafeCaseEnum.EXTRACTION_ERROR:
                    console.print(
                        f"Could not extract any streams for {content_title!r} due to: {exception!r}",
                    )
                    continue

                if status_enum == helpers.SafeCaseEnum.DOWNLOADER_EXCEPTION:
                    console.print(
                        Text(
                            f"Internal downloader error occured for {content_title!r}.",
                        )
                    )
                    continue

        yield {"animes": animes}

def patch(keep_banner: bool = False, log = True):
    f = animdl_download
    if keep_banner: f = (helpers.decorators.banner_gift_wrapper(http_client.client, __core__, check_for_updates=CHECK_FOR_UPDATES))(f)
    if log: f = helpers.decorators.logging_options()(helpers.decorators.setup_loggers()(f))
    animdl.core.cli.commands.download.animdl_download = f

    handle_patch.patch()
