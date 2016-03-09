class PingMod:
    rank = 0
    help_dict = {'py_ping': 'try and guess', 'py_doot': '🎺'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_ping(self):
        await self.client.send_message(self.message.channel, 'pong')

    async def py_doot(self):
        await self.client.send_message(self.message.channel, '🎺           🎺 🎺            🎺🎺 🎺🎺')
