from animdl.core.__version__ import __core__
from animdl.core.codebase.providers import get_provider
from animdl.core.cli import helpers
from animdl.core.cli.http_client import client

def animdl_search(query, provider, **kwargs):
    print(query, provider)

    match, module, _ = get_provider(query, raise_on_failure=True)

    data = {"total": 0, "animes": []}
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
        data["total"] = count
        data["animes"].append(search_data)
    return data

def patch(keep_banner = False, log = True):
    f = animdl_search
    if keep_banner:
        f = helpers.decorators.banner_gift_wrapper()(f)
    if log:
        f = helpers.decorators.setup_loggers()(f)
    import animdl.core.cli.commands.search
    animdl.core.cli.commands.search.animdl_search = f