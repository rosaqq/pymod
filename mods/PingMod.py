class PingMod:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.rank = 0

    async def py_ping(self):
        await self.client.send_message(self.message.channel, 'pong')

