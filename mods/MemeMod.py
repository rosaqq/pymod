class MemeMod:
    rank = 0
    help_dict = {'py_dank': 'dankest memes'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_dank(self, meme):
        await self.client.send_file(self.message.channel, 'memes/' + str(meme) + '.png')
