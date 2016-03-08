class UserMod:
    rank = 0
    help_dict = {'py_usearch': 'searches servers for specified username', 'py_rank': 'returns rank'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_usearch(self, name):
        names = "I found {0} users:"
        name_num = 0
        names_len = 0
        for server in self.client.servers:
            for member in server.members:
                if member.name.lower().find(name.lower()) != -1 and member.id not in names:
                    names += "\n  " + member.name + "  `" + member.id + "`"
                    name_num += 1
                    names_len += len("\n  " + member.name + "  `" + member.id + "`")
        if names_len > 1900:
            await self.client.send_message(self.message.channel,
                                           "The message was too long to send, so I have shortened it and PM'd you")
            await self.client.send_message(self.message.author, names[:1995].format(name_num))
        await self.client.send_message(self.message.channel, names.format(name_num))

    async def py_rank(self, user):
        print(user)
        if user == 'me':
            if self.message.author.id in bot_vars['ranks']:
                await self.client.send_message(self.message.channel,
                                               'Your rank is: ' + str(bot_vars['ranks'][self.message.author.id]))
            else:
                await self.client.send_message(self.message.channel, 'Your rank is: 0')
        else:
            await self.client.send_message(self.message.channel, 'You can only use "me" as args to check your own rank')
