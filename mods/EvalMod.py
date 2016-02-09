class EvalMod:
    rank = 100
    help = "\nEval:\n   eval: does things hopefully\n   aeval: await eval(blah)\n"
    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_eval(self, arg):
        if str(self.message.author.id) == "132694825454665728" or str(self.message.author.id) == "128469181178970112":
            try:
                output = eval(arg)
                await self.client.send_message(self.message.channel, "```python\n" + str(output) + "```")
            except Exception as e:
                await self.client.send_message(self.message.channel, "Something broke with that: " + str(e))

    async def py_aeval(self, arg):
        if str(self.message.author.id) == "132694825454665728" or str(self.message.author.id) == "128469181178970112":
            try:
                output = await eval(arg)
                await self.client.send_message(self.message.channel, "```python\n" + str(output) + "```")
            except Exception as e:
                await self.client.send_message(self.message.channel, "Something broke with that: " + str(e))

