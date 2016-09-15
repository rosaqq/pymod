import configparser
import random

import checks
from discord.ext import commands

config = configparser.ConfigParser()
config.read("pymod.ini")

pymod = commands.Bot(command_prefix='py ', description='hello, I am a potato', pm_help=True)
ranks = {config['GENERAL']['adminID']: '512', config['GENERAL']['adminID2']: '512'}


@pymod.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandError) and ctx.message.channel in checks.allowed_channels:
        await pymod.send_message(ctx.message.channel, 'permission denied')


@pymod.event
async def on_ready():
    print('Logged in as')
    print(pymod.user.name)
    print(pymod.user.id)
    print('------')


@pymod.command(pass_context=True)
@checks.is_admin()
async def come(ctx):
    checks.allowed_channels.append(ctx.message.channel.id)
    await pymod.say('here')


@pymod.command(pass_context=True)
@checks.is_admin()
async def leave(ctx):
    checks.allowed_channels.remove(ctx.message.channel.id)
    await pymod.say('left')


@pymod.command()
@checks.in_channel()
async def add(int1: int, int2: int):
    """[int1] [int2]"""
    await pymod.say(int1 + int2)


@pymod.command()
@checks.in_channel()
async def roll(dice: str):
    """dice = [times]d[die size]
    example: 5d6 = roll 5 6-dice"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await pymod.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await pymod.say(result)


@pymod.command()
@checks.in_channel()
async def choose(*choices: str):
    """choices = [option1] [option2] [etc]
    example: py choose dinner bath me"""
    await pymod.say(random.choice(choices))


pymod.run(config['AUTH']['token'])
