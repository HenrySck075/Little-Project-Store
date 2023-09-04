import discord.http, fake_useragent
from copy import deepcopy

import asyncio
from typing import Any, Iterable, Sequence
from urllib.parse import quote as _uriquote

import aiohttp
from discord.file import File
import discord.utils
from discord.errors import (
    DiscordServerError,
    Forbidden,
    HTTPException,
    NotFound
)
discord.http.HTTPClientOrig = deepcopy(discord.http.HTTPClient) # pyright: ignore
ua = fake_useragent.UserAgent().random

class HTTPUserClient(discord.http.HTTPClientOrig): # pyright: ignore
    def __init__(self, *ok, **nah):
        super().__init__(*ok, **nah)
        self.user_agent = ua

    async def request(
        self,
        route: discord.http.Route,
        *,
        files: Sequence[File] | None = None,
        form: Iterable[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> Any:
        bucket = route.bucket
        method = route.method
        url = route.url

        lock = self._locks.get(bucket)
        if lock is None:
            lock = asyncio.Lock()
            if bucket is not None:
                self._locks[bucket] = lock

        # header creation
        headers: dict[str, str] = {
            "User-Agent": self.user_agent,
        }

        if self.token is not None:
            headers["Authorization"] = self.token
        # some checking if it's a JSON request
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = discord.utils._to_json(kwargs.pop("json"))

        try:
            reason = kwargs.pop("reason")
        except KeyError:
            pass
        else:
            if reason:
                headers["X-Audit-Log-Reason"] = _uriquote(reason, safe="/ ")

        if locale := kwargs.pop("locale", None):
            headers["X-Discord-Locale"] = locale

        kwargs["headers"] = headers
        # Proxy support
        if self.proxy is not None:
            kwargs["proxy"] = self.proxy
        if self.proxy_auth is not None:
            kwargs["proxy_auth"] = self.proxy_auth

        if not self._global_over.is_set():
            # wait until the global lock is complete
            await self._global_over.wait()

        response: aiohttp.ClientResponse | None = None
        data: dict[str, Any] | str | None = None
        await lock.acquire()
        with discord.http.MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):
                if files:
                    for f in files:
                        f.reset(seek=tries)

                if form:
                    form_data = aiohttp.FormData(quote_fields=False)
                    for params in form:
                        form_data.add_field(**params)
                    kwargs["data"] = form_data

                try:
                    async with self.__session.request(
                        method, url, **kwargs
                    ) as response:

                        # even errors have text involved in them so this is safe to call
                        data = await discord.http.json_or_text(response)

                        # check if we have rate limit header information
                        remaining = response.headers.get("X-Ratelimit-Remaining")
                        if remaining == "0" and response.status != 429:
                            # we've depleted our current bucket
                            delta = discord.utils._parse_ratelimit_header(
                                response, use_clock=self.use_clock
                            )
                            maybe_lock.defer()
                            self.loop.call_later(delta, lock.release)

                        # the request was successful so just return the text/json
                        if 300 > response.status >= 200:
                            return data

                        # we are being rate limited
                        if response.status == 429:
                            if not response.headers.get("Via") or isinstance(data, str):
                                # Banned by Cloudflare more than likely.
                                raise HTTPException(response, data)

                            fmt = (
                                "We are being rate limited. Retrying in %.2f seconds."
                                ' Handled under the bucket "%s"'
                            )

                            # sleep a bit
                            retry_after: float = data["retry_after"]

                            # check if it's a global rate limit
                            is_global = data.get("global", False)
                            if is_global:
                                self._global_over.clear()

                            await asyncio.sleep(retry_after)

                            # release the global lock now that the
                            # global rate limit has passed
                            if is_global:
                                self._global_over.set()

                            continue

                        # we've received a 500, 502, or 504, unconditional retry
                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # the usual error cases
                        if response.status == 403:
                            raise Forbidden(response, data)
                        elif response.status == 404:
                            raise NotFound(response, data)
                        elif response.status >= 500:
                            raise DiscordServerError(response, data)
                        else:
                            raise HTTPException(response, data)

                # This is handling exceptions from the request
                except OSError as e:
                    # Connection reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

            if response is not None:
                # We've run out of retries, raise.
                if response.status >= 500:
                    raise DiscordServerError(response, data)

                raise HTTPException(response, data)

            raise RuntimeError("Unreachable code in HTTP handling")


    def __repr__(self) -> str:
        return "discord.http.HTTPClient (patched)"

setattr(discord.http, "HTTPClient", HTTPUserClient)
print(discord.http.__dict__)

