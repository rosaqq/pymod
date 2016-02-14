class RankMod:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.rank = 100

    async def py_rank(self, user, rank):
        a = user.replace('<@', '')
        b = a.replace('>', '')
        bot_vars['ranks'][b] = int(rank)
        await self.client.send_message(self.message.channel, 'set ' + user + "'s rank to " + rank)
