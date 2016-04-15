class ModerationMod:
    rank = 100
    help_dict = {'py_purge': 'deletes <num> messages from [mention] user'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_purge(self, num, user=None):
        if self.message.mentions:
            msgs = [m for m in self.client.logs_from(self.message.channel) if m.author in self.message.mentions and m is not self.message][::-1]
            for i in range(int(num)):
                try:
                    await self.client.delete_message(msgs[i])
                except IndexError:
                    pass
            await self.client.send_message(self.message.channel, "Purged " + num + " messages from this channel")
            await self.client.delete_message(self.message)

        else:
            msgs = self.client.logs_from(self.message.channel)
            msgs.remove(self.message)
            for i in range(int(num)):
                try:
                    await self.client.delete_message(msgs[i])
                except IndexError:
                    pass
            await self.client.send_message(self.message.channel, "Purged " + num + " messages from this channel")
            await self.client.delete_message(self.message)
