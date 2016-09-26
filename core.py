import configparser
import os
import pickle
import random
from types import FunctionType

import discord
import sys

from discord.ext import commands

import checks

client = discord.Client()
config = configparser.ConfigParser()
config.read('pymod.ini')
bot_vars = {}


# persistence
# ----------------------------------------------------------------------------------------------------------------------
def save():
    with open('bot_vars.pickle', 'wb') as save_file:
        pickle.dump(bot_vars, save_file)
        save_file.close()


def load():
    global bot_vars
    try:
        with open('bot_vars.pickle', 'rb') as save_file:
            bot_vars = pickle.load(save_file)
            save_file.close()
    except IOError:
        admin1, admin2 = config['GENERAL']['adminID'], config['GENERAL']['adminID2']
        bot_vars = {'ranks': {admin1: 512, admin2: 512}, 'allowed_channels': [],
                    'cmd_dict': {}, 'callsign': {'default': 'py'},
                    'base_cmds': {'py_come': 128, 'py_leave': 128, 'py_callme': 512, 'py_botvars': 512,
                                  'py_eval': 512, 'py_aeval': 512, 'py_exec': 512, 'py_help': 0}}
        save()


def reset():
    os.remove('bot_vars.pickle')
    load()


# ----------------------------------------------------------------------------------------------------------------------


# module loader
# ----------------------------------------------------------------------------------------------------------------------
def load_modules():
    global bot_vars

    bot_vars['cmd_dict'] = {}
    files = os.listdir('mods')
    sys.path.append('mods')
    for j in files:
        if j.endswith('.py'):
            i = j[0:-3]
            exec("globals()['" + i + "'] = __import__('" + i + "')." + i)
            funcs = [x for x, y in eval(i + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]
            bot_vars['cmd_dict'][i] = funcs


# ----------------------------------------------------------------------------------------------------------------------


# parser
# ----------------------------------------------------------------------------------------------------------------------
def parse(message):
    try:
        server_callsign = bot_vars['callsign'][str(message.server.id)]
    except (KeyError, AttributeError):
        server_callsign = bot_vars['callsign']['default']

    if message.content.startswith(server_callsign):
        cmd_args = message.content.replace(server_callsign, 'py').split()
        cmd = '_'.join(cmd_args[0:2])
        args = [x for x in cmd_args[2:len(cmd_args)]]
        for asd in args:
            args[args.index(asd)] = \
                args[args.index(asd)].replace('\\n', '\n').replace('\\t', '\t').replace('\\s', '\u0020')
        return cmd, args
    else:
        return 'wrong_callsign', []


# ----------------------------------------------------------------------------------------------------------------------


# base commands
# ----------------------------------------------------------------------------------------------------------------------
async def py_come(message):
    """Enable bot in the current channel."""
    if message.channel.id in bot_vars['allowed_channels']:
        await client.send_message(message.channel, 'channel already enabled')
    else:
        bot_vars['allowed_channels'].append(message.channel.id)
        await client.send_message(message.channel, 'channel enabled')
    save()


async def py_leave(message):
    """Disable bot in the current channel."""
    if message.channel.id in bot_vars['allowed_channels']:
        bot_vars['allowed_channels'].remove(message.channel.id)
        await client.send_message(message.channel, 'channel disabled')
    else:
        await client.send_message(message.channel, 'channel already disabled')
    save()


async def py_callme(message, callsign):
    """Change the bot callsign; usage example: py callme <new_callsign>
    Not available on private message interaction."""
    if message.server is not None:
        bot_vars['callsign'][str(message.server.id)] = str(callsign)
        name = 'pymod (' + str(callsign) + ')'
        await client.change_nickname(message.server.me, name)
        await client.send_message(message.channel, 'new callsign: ' + str(callsign))
        save()
    else:
        await client.send_message(message.channel, 'Command not supported in a private channel.')


async def py_botvars(message):
    """Prints the current botvars, a python dictionary pymod uses to store it's variables."""
    await client.send_message(message.channel, bot_vars)


async def py_eval(message, *args):
    """Evaluates an expression; usage example: py eval 5+5"""
    try:
        await client.send_message(message.channel, '```' + str(eval(' '.join(args))) + '```')
    except Exception as lol:
        await client.send_message(message.channel, lol)


async def py_aeval(message, *args):
    """Same as eval, but for when the expression passed in evaluates to a coroutine."""
    try:
        await eval(' '.join(args))
    except Exception as lol:
        await client.send_message(message.channel, lol)


async def py_exec(message, *args):
    """Interprets args as python code"""
    try:
        code = ' '.join(args)
        print(str(message.timestamp) + ' [' + message.author.name +
              '] executed:\n--------------------------------\n' + code +
              '\n--------------------------------\nwith output:')
        exec(code)
        print('\n')
        await client.send_message(message.channel, 'code executed')
    except Exception as lol:
        await client.send_message(message.channel, lol)


async def py_help(message):
    """Prints this message."""

    helplist = {}
    user_rank = get_rank(message)

    for func in bot_vars['base_cmds']:
        if user_rank >= bot_vars['base_cmds'][func]:
            helplist[func] = eval(func + '.__doc__')

    for key in bot_vars['cmd_dict']:
        if user_rank >= eval(key + '.rank'):
            for func in bot_vars['cmd_dict'][key]:
                helplist[func] = eval(key + '.help_dict[func]')

    help_array = []
    for func in helplist:
        help_array.append('#' + func + ':\n\t' + helplist[func])

    msg = 'Available commands are: ```Markdown\n' + '\n'.join(help_array) + '```\n( _ represents a ' \
                                                                            'space and "py" should be replaced ' \
                                                                            'by the current callsign)'
    return await client.send_message(message.author, msg)


# ----------------------------------------------------------------------------------------------------------------------


def get_rank(message):
    if message.author.id in bot_vars['ranks']:
        return bot_vars['ranks'][message.author.id]
    else:
        return 0


load()
load_modules()
print('bot_vars pre-set to: ' + str(bot_vars))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    cmd, args = parse(message)
    user_rank = get_rank(message)

    if cmd in bot_vars['base_cmds'] and user_rank >= bot_vars['base_cmds'][cmd]:

        try:
            await eval(cmd + '(message, *args)')
        except Exception as fail:
            msg = 'Something went wrong:\n' + str(fail)
            await client.send_message(message.channel, msg)

    elif message.channel.id in bot_vars['allowed_channels']:

        try:
            # check in modules
            for key in bot_vars['cmd_dict']:
                if cmd in bot_vars['cmd_dict'][key]:
                    if user_rank >= eval(key + '.rank'):
                        exec('a = ' + key + '(client, message)')
                        await eval('a.' + cmd + '(*args)')
                        exec('del a')
                    else:
                        await client.send_message(message.channel, 'permission denied')

        except Exception as retard:
            msg = 'Something went wrong:\n' + str(retard)
            await client.send_message(message.channel, msg)


client.run(config['AUTH']['token'])