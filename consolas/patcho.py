import discord.http, textwrap, fake_useragent, inspect
from copy import deepcopy

discord.http.HTTPClientOrig = deepcopy(discord.http.HTTPClient) # pyright: ignore

class HTTPUserClient(discord.http.HTTPClientOrig): # pyright: ignore
    def __init__(self, *ok, **nah):
        super().__init__(*ok, **nah)
        self.user_agent = "hi" 

requestCode = textwrap.dedent(inspect.getsource(discord.http.HTTPClient.request).replace('f"Bot {{self.token}}"','self.token'))

async def request():...

exec(requestCode,globals())

HTTPUserClient.request=request
discord.http.HTTPClient = HTTPUserClient
