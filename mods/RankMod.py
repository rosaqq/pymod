class RankMod:
    rank = 100
    help_dict = {'py_rank': 'set a user1\'s rank'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_setrank(self, user, rank):
        a = user.replace('<@', '')
        b = a.replace('>', '')
        bot_vars['ranks'][b] = int(rank)
        await self.client.send_message(self.message.channel, 'set ' + user + "'s rank to " + rank)

