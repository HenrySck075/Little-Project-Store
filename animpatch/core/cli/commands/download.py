from pathlib import Path

from typing import Dict

from rich.text import Text

from animdl.core.__version__ import __core__
from animdl.core.codebase import providers, sanitize_filename
from animdl.core.config import (
    AUTO_RETRY,
    DEFAULT_PROVIDER
)
import animdl.core.cli.helpers as helpers, animdl.core.cli.http_client as http_client

import animdl.core.cli.commands.download, logging

from ....exc import DownloaderException, ExtractionError, NoContentFound
from ....helpers import DisabledLogger, addKwargs

def animdl_download(
    query, special, quality, download_dir, idm, index, log_level, **kwargs
) -> Dict[str, list]:
    r = kwargs.get("range")

    log = kwargs.get("logging", False)

    console = helpers.stream_handlers.get_console(log)

    logger = logging.getLogger("downloader") if log else DisabledLogger("downloader", log_level)

    progress_callback = kwargs.get("progress_callback", lambda prog, total: "")

    anime, provider = helpers.process_query(
        http_client.client, query, console, auto_index=index, provider=DEFAULT_PROVIDER
    )

    if not anime:
        raise NoContentFound("Could not find an anime of that name :/.")

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
            raise NoContentFound("Could not find any streams on the site :/.\nThis could mean that, either those episodes are unavailable or that the scraper has broke.")

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

                try: 
                    file_path = helpers.safe_download_callback( # patch this to not log the progress created by tqdm
                        session=http_client.client,
                        logger=logger,
                        stream_urls=stream_urls,
                        quality=quality,
                        expected_download_path=expected_download_path,
                        use_internet_download_manager=idm,
                        retry_timeout=AUTO_RETRY,
                        log_level=log_level,
                        progress_callback=progress_callback
                    )
                except NoContentFound:
                    animes[content_name]["episodes"][content_title]["exception"] = NoContentFound(f"Could not find any streams for {content_title!r}")

                except ExtractionError as e:
                    animes[content_name]["episodes"][content_title]["exception"] = ExtractionError(f"Could not extract any streams for {content_title!r} due to: {' '.join(e.args)!r}")

                except DownloaderException:
                    animes[content_name]["episodes"][content_title]["exception"] = DownloaderException(f"Internal downloader error occured for {content_title!r}.")
                
                except Exception:
                    animes[content_name]["episodes"][content_title]["path"] = ""
                
                else:
                    animes[content_name]["episodes"][content_title]["path"] = file_path
                    animes[content_name]["episodes"][content_title]["exception"] = None

        return {"animes": animes}

def patch(keep_banner: bool = False, log = True):
    f = animdl_download
    if keep_banner: f = helpers.decorators.banner_gift_wrapper()(f)
    if log: f = helpers.decorators.setup_loggers()(addKwargs(logging=True)(f))
    
    animdl.core.cli.commands.download.animdl_download = f

