import random

class FlipMod:
    rank = 0
    help_dict = {'py_flip': 'seperated by space', 'py fiip': 'shh'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_flip(self, *args):
        await self.client.send_message(self.message.channel, random.choice(args))

    async def py_fiip(self, *args):
        await self.client.send_message(self.message.channel, args[0])
