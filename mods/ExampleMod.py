class ExampleMod:

    rank = 0
    help_dict = {'py_exmod': 'Command from an example module.'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_exmod(self):
        await self.message.channel.send('Thanks for using the example module. That\'s all.')
