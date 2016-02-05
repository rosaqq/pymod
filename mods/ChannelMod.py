class ChannelMod:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.allowed_channels = []

    async def py_come(self):
        self.allowed_channels.append(self.message.channel.id)

    async def py_leave(self):
        self.allowed_channels.remove(self.message.channel.id)
