from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('pymod.ini')


allowed_channels = []


def is_admin():
    def predicate(ctx):
        return ctx.message.author.id == config['GENERAL']['adminID'] or config['GENERAL']['adminID2']
    return commands.check(predicate)


def in_channel():
    def predicate(ctx):
        return ctx.message.channel.id in allowed_channels
    return commands.check(predicate)
