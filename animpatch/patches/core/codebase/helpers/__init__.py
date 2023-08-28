import re

def construct_site_based_regex(
    site_url: "str", *, extra: "str" = "", extra_regex: "str" = ""
):
    return re.compile(site_url)

def patch():
    import animdl.core.codebase.helpers
    animdl.core.codebase.helpers.construct_site_based_regex = construct_site_based_regex