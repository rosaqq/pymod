class PingMod:
    rank = 0
    help_dict = {'py_ping': 'try and guess'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_ping(self):
        await self.client.send_message(self.message.channel, 'pong')
