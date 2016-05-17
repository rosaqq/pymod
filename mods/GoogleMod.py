from urllib import request
import json
import configparser

config = configparser.ConfigParser()
config.read('google.ini')


class GoogleMod:
    rank = 0
    help_dict = {'py_search': 'search google'}
    global blacklist
    blacklist = __import__('GoogleBlacklistMod').blacklist

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.filter = __import__('GoogleBlacklistMod').filter
        self.key = config['AUTH']['key']

    async def py_search(self, *args):
        global blacklist
        for i in args:
            if (i in blacklist) and self.filter:
                raise Exception("Search term in blacklist: " + i)
        query = '+'.join(args)
        base = "https://www.googleapis.com/customsearch/v1?cx=006104278528152025374%3Ar7ai6-zcpb4&" \
               "key={}&q=".format(self.key)
        with request.urlopen(base + query) as r:
            results = json.loads(r.read().decode(r.headers.get_content_charset('utf-8')))
        # res = request.urlopen(base + query)
        # string = response.read(res).decode('utf-8')
        # results = json.loads(str(res))
        if "items" in results:
            err = False
            errterm = ""
            for i in blacklist:
                if (i in results["items"][0]["link"] or i in results["items"][0]["link"] or
                            i in results["items"][0]["snippet"]) and self.filter:
                    err = True
                    errterm = i
            if not err:
                await self.client.send_message(self.message.channel, "`" + str(results["items"][0]["title"]) + "`\n" +
                                               str(results["items"][0]["snippet"]) +
                                               "\nLink: " + str(results["items"][0]["link"]))
            else:
                raise Exception("Blacklisted term in search result: " + errterm)
        else:
            await self.client.send_message(self.message.channel, "Couldn't find anything ;-;")

    # async def py_g(self, *args):
    #     raise Exception("it's broken")
