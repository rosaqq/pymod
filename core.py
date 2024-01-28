import configparser
import os
import sys
import pickle
from types import FunctionType

import discord

# todo: read up on what the frick intents are
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
        admin1, admin2 = int(config['GENERAL']['adminID']), int(config['GENERAL']['adminID2'])
        bot_vars = {
            'ranks': {admin1: 512, admin2: 512}, 'allowed_channels': [],
            'cmd_dict': {}, 'callsign': {'default': 'py'},
            'base_cmds': {
                'py_come': 128, 'py_leave': 128, 'py_callme': 512, 'py_startclean': 128, 'py_stopclean': 128,
                'py_botvars': 512, 'py_eval': 512, 'py_aeval': 512, 'py_exec': 512, 'py_help': 0
            },
            'autoclean_user_id': int(config['GENERAL']['autoclean_user_id']),
            'autoclean': 1
        }
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
        return '', []


# ----------------------------------------------------------------------------------------------------------------------


# base commands
# ----------------------------------------------------------------------------------------------------------------------
async def py_come(message):
    """Enable bot in the current channel."""
    if message.channel.id in bot_vars['allowed_channels']:
        await message.channel.send('channel already enabled')
    else:
        bot_vars['allowed_channels'].append(message.channel.id)
        await message.channel.send('channel enabled')
    save()


async def py_leave(message):
    """Disable bot in the current channel."""
    if message.channel.id in bot_vars['allowed_channels']:
        bot_vars['allowed_channels'].remove(message.channel.id)
        await message.channel.send('channel disabled')
    else:
        await message.channel.send('channel already disabled')
    save()


async def py_callme(message, callsign):
    """Change the bot callsign; usage example: py callme <new_callsign>
    Not available on private message interaction."""
    if message.server is not None:
        bot_vars['callsign'][str(message.server.id)] = str(callsign)
        name = 'pymod (' + str(callsign) + ')'
        await message.server.me.edit(nick=name)
        await message.channel.send('new callsign: ' + str(callsign))
        save()
    else:
        await message.channel.send('Command not supported in a private channel.')


async def py_startclean(message):
    """Toggle on auto clean msgs"""
    bot_vars['autoclean'] = 1
    await message.channel.send('Autoclean is ' + str(bot_vars['autoclean']))


async def py_stopclean(message):
    """Toggle off auto clean"""
    bot_vars['autoclean'] = 0
    await message.channel.send('Autoclean is ' + str(bot_vars['autoclean']))


async def py_botvars(message):
    """Prints the current botvars, a python dictionary pymod uses to store its variables."""
    await message.channel.send(bot_vars)


async def py_eval(message, *args):
    """Evaluates an expression; usage example: py eval 5+5"""
    try:
        await message.channel.send('```' + str(eval(' '.join(args))) + '```')
    except Exception as lol:
        await message.channel.send(lol)


async def py_aeval(message, *args):
    """Same as eval, but for when the expression passed in evaluates to a coroutine."""
    try:
        await eval(' '.join(args))
    except Exception as lol:
        await message.channel.send(lol)


async def py_exec(message, *args):
    """Interprets args as python code"""
    try:
        code = ' '.join(args)
        print(str(message.timestamp) + ' [' + message.author.name +
              '] executed:\n--------------------------------\n' + code +
              '\n--------------------------------\nwith output:')
        exec(code)
        print('\n')
        await message.channel.send('code executed')
    except Exception as lol:
        await message.channel.send(lol)


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
        help_array.append('#' + func.replace('_', ' ') + '\n\t' + helplist[func] + '\n')

    msg = 'Available commands are: ```md\n' + '\n'.join(help_array) + '```\n("#py" should be replaced ' \
                                                                      'by the current callsign)'
    return await message.author.send(msg)


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


# Used in on_message to keep track of potential bot triggers
last_bot_trigger: discord.Message


@client.event
async def on_message(message):
    cmd, args = parse(message)
    user_rank = get_rank(message)

    # Save a message if it looks like a bot trigger
    # (Bot replies do not start with these chars, so they won't overwrite)
    global last_bot_trigger
    if message.content[0] in ['.', '!', '-']:
        last_bot_trigger = message

    # NO CALL SIGN
    if not cmd:
        # If autoclean is on, always work in any channel
        if bot_vars['autoclean'] and message.author.id == bot_vars['autoclean_user_id']:
            await message.delete()

            # also delete trigger message
            if last_bot_trigger is not None:
                await last_bot_trigger.delete()

    # CALL SIGN WAS USED
    else:
        if cmd in bot_vars['base_cmds'] and user_rank >= bot_vars['base_cmds'][cmd]:

            try:
                await eval(cmd + '(message, *args)')
            except Exception as fail:
                msg = 'Something went wrong:\n' + str(fail)
                await message.channel.send(msg)

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
                            await message.channel.send('permission denied')

            except Exception as retard:
                msg = 'Something went wrong:\n' + str(retard)
                await message.channel.send(msg)


client.run(config['AUTH']['token'])
