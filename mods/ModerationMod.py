class ModerationMod:
    rank = 100
    help_dict = {'py_purge': 'deletes <num> messages from [mention] user'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_purge(self, num):
        if self.message.mentions:
            msgs = [m for m in self.client.messages if m.author in self.message.mentions and m.channel == self.message.channel]
            for i in range(int(num)):
                try:
                    await self.client.delete_message(msgs[i])
                except IndexError:
                    pass

        else:
            msgs = [m for m in self.client.messages if m.channel == self.message.channel]
            for i in range(int(num)):
                try:
                    await self.client.delete_message(msgs[i])
                except IndexError:
                    pass
