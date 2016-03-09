from urllib import request
import json
import random


class ReactionMod:
    rank = 100
    help_dict = {'py_gif': 'ok I guess you can use this if you hate giphy or something'}  # No idea why I made this or if it even works.

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_gif(self, tag):
        base = "http://replygif.net/api/gifs?api-key=39YAprx5Yi&tag="
        with request.urlopen(base + tag) as r:
            results = json.loads(r.read().decode(r.headers.get_content_charset('utf-8')))
        if results:
            gif = random.choice(results)
            await self.client.send_message(self.message.channel, "<@" + self.message.author.id + "> " + gif["file"])
        else:
            await self.client.send_message(self.message.channel,
                                           "<@" + self.message.author.id + ">, I couldn't find anything matching " +
                                           tag + ", sorry!")
