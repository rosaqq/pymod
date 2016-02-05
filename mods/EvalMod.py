from gvar import pyvars


class EvalMod:
    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_eval(self, code):
        try:
            await self.client.send_message(self.message.channel, '```' + str(eval(code)) + '```')
        except Exception as lol:
            await self.client.send_message(self.message.channel, lol)
