import pickle
import humanfriendly


class GoogleBlacklistMod:
    rank = 100
    help_dict = {'py_addblacklist': 'add to the search blacklist', 'py_blacklist': 'prints blacklist',
                 'py_remblacklist': 'remove from search blacklist', 'py_replaceblacklist': 'replace entire blacklist'}
    global blacklist
    try:
        with open('blacklist.pickle', 'rb') as save_file:
            blacklist = pickle.load(save_file)
            save_file.close()
    except IOError:
        blacklist = ['porn']
    except EOFError:
        blacklist = ['porn']
    global filter
    filter = True

    def __init__(self, client, message):
        self.client = client
        self.message = message


    async def py_addblacklist(self, *words):
        global blacklist
        for i in words:
            blacklist.append(i)
            await self.client.send_message(self.message.channel, "Search blacklist has been updated")
            self.save()


    async def py_blacklist(self):
        global blacklist
        if blacklist:
            await self.client.send_message(self.message.channel, "Current search blacklist: " + ", ".join(blacklist))
        else:
            await self.client.send_message(self.message.channel, "My search blacklist is empty :/")

    async def py_remblacklist(self, *words):
        global blacklist
        err = 0
        for word in words:
            if word in blacklist:
                blacklist.remove(word)
            else:
                err += 1
        if err != len(words):
            await self.client.send_message(self.message.channel, "Search blacklist has been updated with " + str(err) +
                                           " errors")
            self.save()
        else:
            await self.client.send_message(self.message.channel, "Search blacklist has not been updated: words are "
                                                                 "already absent from blacklist")

    async def py_filter(self, opt):
        global filter
        try:
            if humanfriendly.coerce_boolean(opt):
                if filter:
                    await self.client.send_message(self.message.channel, "I am already filtering NSFW results, silly")
                else:
                    filter = True
                    await self.client.send_message(self.message.channel, "I'll try to keep your eyes pure")
            else:
                if filter:
                    filter = False
                    await self.client.send_message(self.message.channel, "*Fine*...I *guess* I'll show you weird stuff"
                                                                         " :/")
                else:
                    await self.client.send_message(self.message.channel, "I'm already showing you weird stuff, silly")
        except ValueError:
            await self.client.send_message(self.message.channel, "Idk what you want me to do! Yes or no?")

    def save(self):
        global blacklist
        with open('blacklist.pickle', 'wb') as save_file:
            pickle.dump(blacklist, save_file)
            save_file.close()
