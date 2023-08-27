import click

from animdl.core.__version__ import __core__
from animdl.core.codebase.helpers import optopt
from animdl.core.codebase.providers import get_provider
from animdl.core.config import CHECK_FOR_UPDATES, DEFAULT_PROVIDER
from animdl.core.cli import helpers
from animdl.core.cli.http_client import client


@helpers.decorators.logging_options()
@helpers.decorators.setup_loggers()
@helpers.decorators.banner_gift_wrapper(
    client, __core__, check_for_updates=CHECK_FOR_UPDATES
)
def animdl_search(query, json, provider, **kwargs):

    console = helpers.stream_handlers.get_console()

    match, module, _ = get_provider(query, raise_on_failure=False)

    if module is not None:
        genexp = (
            {
                "name": (
                    module.metadata_fetcher(client, query, match)["titles"] or [None]
                )[0]
                or "",
                "anime_url": query,
            },
        )
    else:
        genexp = helpers.provider_searcher_mapping.get(provider)(client, query)

    for count, search_data in enumerate(genexp, 1):
        if json:
            print(optopt.jsonlib.dumps(search_data))
        else:
            console.print(
                f"{count}. {search_data['name']} / {search_data['anime_url']}"
            )
