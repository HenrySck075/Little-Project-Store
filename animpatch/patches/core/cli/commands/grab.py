import json

import click

from animdl.core.__version__ import __core__
from animdl.core.codebase import providers
from animdl.core.config import DEFAULT_PROVIDER
from animdl.core.cli import helpers
from animdl.core.cli.http_client import client

console = None
def animdl_grab(query, index, **kwargs):
    "Send the stream links for external usage."

    console.print(
        "The content is outputted to [green]stdout[/] while these messages are outputted to [red]stderr[/]."
    )

    anime, provider = helpers.process_query(
        client, query, console, auto_index=index, provider=DEFAULT_PROVIDER
    )

    if not anime:
        return

    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url"), check=kwargs.get("range")
    ):
        stream_url = list(helpers.ensure_extraction(client, stream_url_caller))
        click.echo(json.dumps({"episode": episode, "streams": stream_url}))

def patch(keep_banner = False, log = True):
    f = animdl_grab
    if keep_banner:
        console = helpers.stream_handlers.get_console(log)
        f = helpers.decorators.banner_gift_wrapper(console=console)(f)
    if log:
        f = helpers.decorators.setup_loggers(f)