from urllib import request
import json


class GoogleMod:
    rank = 0
    help_dict = {'py_search': 'search google'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_search(self, *args):
        query = '+'.join(args)
        base = "https://www.googleapis.com/customsearch/v1?cx=006104278528152025374%3Ar7ai6-zcpb4&key=AIzaSyANTJTh7HtxQvtPxCSNdNVyRiZWTWqLi94&q="
        with request.urlopen(base + query) as r:
            results = json.loads(r.read().decode(r.headers.get_content_charset('utf-8')))
        # res = request.urlopen(base + query)
        # string = response.read(res).decode('utf-8')
        # results = json.loads(str(res))
        if "items" in results:
            await self.client.send_message(self.message.channel, "`" + str(results["items"][0]["title"]) + "`\n" + str(
                    results["items"][0]["snippet"]) + "\nLink: " + str(results["items"][0]["link"]))
        else:
            await self.client.send_message(self.message.channel, "Couldn't find anything ;-;")
