import discord
class NowPlayingMod:
    rank = 75
    help_dict = {'py_np': 'changes "Playing:" message'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_np(self, *status):
        if status[0].lower() == "none":
            game = None
        else:
            game = discord.Game(name=' '.join(status))
        await self.client.change_status(game=game)
