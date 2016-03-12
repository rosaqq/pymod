import time
import asyncio

class PingMod:
    rank = 0
    help_dict = {'py_ping': 'try and guess', 'py_doot': '🎺', 'py_chomp': '2meme', 'py_pls': ':/', 'py_bestmod': 'beno',
                 'py_picklepls': 'pickle, pls'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_ping(self):
        await self.client.send_message(self.message.channel, 'pong')
        async def pong(msg):
            if msg.content == "Pong" and msg.author == self.bot.user:
                await self.client.send_message(msg.channel, ":thumbsup: Delay: " + str(round(time.time()*1000) - now) + "ms")
                self.client.remove_listener(pong, name="on_message")

        now = round(time.time()*1000)
        self.client.add_listener(pong, name="on_message")
        await self.client.say("Pong")
        self.client.remove_listener(pong, name="on_message")

    async def py_doot(self):
        await self.client.send_message(self.message.channel, '🎺           🎺 🎺            🎺🎺 🎺🎺')

    async def py_chomp(self):
        # inside-meme
        if str(self.message.server.id) == "133421848103878656":
            await self.client.send_message(self.message.channel, "https://youtu.be/w5JICa_ZxBk")
        else:
            raise Exception("⚠Meme too spicy⚠")

    async def py_pls(self):
        await self.client.send_message(self.message.channel, 'Sorry :/')

    async def py_bestmod(self):
        await self.client.send_message(self.message.channel, 'Everyone knows beno is best mod')

    async def py_picklepls(self):
        await self.client.send_message(self.message.channel, 'https://i.imgur.com/5NX0Wnk.png')
