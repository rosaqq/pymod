import discord
import time

class InfoMod:
    rank = 0
    help_dict = {'py_info': 'basic bot info', 'py_owner': 'Who owns this bot? (hint: Ako)'}
    owner = "<@132694825454665728>"
    version = "1.0"
    api = "discord.py " + str(discord.__version__)

    def __init__(self, client, message):
        self.client = client
        self.message = message
        # self.uptime = time.time() - pymod.start_time


    async def py_info(self):
        await self.client.send_message(self.message.channel, "**00Unit - v" + InfoMod.version + "**\nI am a discord bot "
                                                             "written in python with " + InfoMod.api + "\n"
                                                             + InfoMod.owner + " is my owner. @secknv put together most of"
                                                             " my core\nThis is pretty short because Ako can't figure "
                                                             "out how tf to get into my core from here :/")

    async def py_owner(self):
        await self.client.send_message(self.message.channel, "My owner is " + InfoMod.owner)
