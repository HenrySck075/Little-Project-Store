import functools
from animdl.core.cli.helpers.constants import SOURCE_REPOSITORY
import animdl.core.cli.helpers.banner as banner
from animdl.core.cli.http_client import client
from animdl.core.config import CHECK_FOR_UPDATES
from animdl.core.__version__ import __core__

def iter_banner(
    session,
    current_version,
    *,
    check_for_updates=True,
    description="A highly efficient, powerful and fast anime scraper.",
):

    author, repository_name = SOURCE_REPOSITORY

    yield (f"{author}/{repository_name} - v{current_version}")
    yield ("HenrySck075/animpatch (Part of Little-Project-Store repo)")
    yield (description)

    if check_for_updates:

        upstream_version = banner.fetch_upstream_version(session)

        tuplised_upstream, tuplised_current_version = tuple(
            upstream_version.split(".")
        ), tuple(current_version.split("."))

        if tuplised_upstream > tuplised_current_version:
            yield (f"Update ↑ {upstream_version} ↓ {current_version}")
            yield (f"To update, use: pip install --upgrade animdl")

def patch():
    banner.iter_banner = iter_banner 
    banner.banner_gift_wrapper = functools.partial(banner.banner_gift_wrapper, client, __core__, check_for_updates=CHECK_FOR_UPDATES) #fuck