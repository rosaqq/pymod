import os
import urllib.request


class MemeMod:
    rank = 0
    help_dict = {'py_dank': 'dankest memes', 'py_addmeme': 'add a dankest meme: py addmeme [name] [imgurl]'}

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.folder = 'memes'
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    async def py_dank(self, meme):
        await self.client.send_file(self.message.channel, 'memes/' + str(meme) + '.png')

    async def py_addmeme(self, name, img_url):
        new_name = str(name) + '.png'
        urllib.request.urlretrieve(img_url, self.folder + '/' + new_name)