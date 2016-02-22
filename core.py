import discord
import sys
import os
import configparser
from types import FunctionType
import inspect


# natives loader
# ----------------------------------------------------------------------------------------------------------------------
def load_natives():
    exec("globals()['natives'] = __import__('natives')")
    bot_vars['natives'] = {}
    native_classes = [x for x, y in natives.__dict__.items() if 'Pyc' in x]
    for i in native_classes:
        bot_vars['natives'][i] = [x for x, y in eval('natives.' + i + '.__dict__.items()')
                                  if type(y) == FunctionType and 'py_' in x]


# ----------------------------------------------------------------------------------------------------------------------


# module loader
# ----------------------------------------------------------------------------------------------------------------------
def load_modules():
    bot_vars['cmd_dict'] = {}
    files = os.listdir('mods')
    sys.path.append('mods')
    for j in files:
        if j.endswith('.py'):
            i = j[0:-3]
            exec("globals()['" + i + "'] = __import__('" + i + "')." + i)
            bot_vars['cmd_dict'][i] = \
                [x for x, y in eval(i + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]


# ----------------------------------------------------------------------------------------------------------------------


# reset function
# ----------------------------------------------------------------------------------------------------------------------
def py_reset(args):
    if args == 'mods':
        load_modules()
        return 'modules reloaded'
    elif args == 'nats':
        load_natives()
        return 'natives reloaded'
    elif args == 'full':
        natives.reset()
        load_natives()
        load_modules()
        return 'full reset complete'
    else:
        return 'invalid args: use py reset $full/$mods/$nats'


# ----------------------------------------------------------------------------------------------------------------------
print('Connecting to discord servers...')

client = discord.Client()
config = configparser.ConfigParser()
config.read("pymod.ini")
load_natives()
load_modules()
print('bot_vars pre-set to: ' + str(bot_vars))


@client.event
async def on_message(message):
    cmd, args = natives.parse(message)
    helpcmd = False
    listing = []

    if cmd == 'py_come' or cmd == 'py_leave' or message.channel.id in bot_vars['allowed_channels']:
        try:
            user_rank = bot_vars['ranks'][message.author.id]
        except KeyError:
            user_rank = 0

        if user_rank >= 100 and cmd == 'py_reset':
            try:
                await client.send_message(message.channel, eval('py_reset(*args)'))
            except Exception as fml:
                await client.send_message(message.channel, fml)
        else:
            try:
                # check if cmd in natives
                for key in bot_vars['natives']:
                    if cmd in bot_vars['natives'][key]:
                        nat = True
                        exec('a = natives.' + key + '(client, message)')
                        if user_rank >= eval('a.rank'):
                            await eval('a.' + cmd + '(*args)')
                        else:
                            await client.send_message(message.channel, 'permission denied')
                    elif cmd == 'py_help':
                        helpcmd = True
                        exec('a = natives.' + key + '(client, message)')
                        if user_rank >= eval('a.rank'):
                            for thing in bot_vars['natives'][key]:
                                listing.append(thing)
                # check in modules
                for key in bot_vars['cmd_dict']:
                    if cmd in bot_vars['cmd_dict'][key]:
                        nat = False
                        exec('a = ' + key + '(client, message)')
                        if user_rank >= eval('a.rank'):
                            await eval('a.' + cmd + '(*args)')
                        else:
                            await client.send_message(message.channel, 'permission denied')
                    elif cmd == 'py_help':
                        helpcmd = True
                        exec('a = ' + key + '(client, message)')
                        if user_rank >= eval('a.rank'):
                            for thing in bot_vars['cmd_dict'][key]:
                                listing.append(thing)
                if helpcmd:
                    helpmsg = 'Available commands are: ```\n' + '\n'.join(
                                listing) + '```\nUse $x in the command to pass ' \
                                           'parameter x to a function that ' \
                                           'requires it.'
                    await client.send_message(message.author, helpmsg)

            # I know this is retarded but only very rarely it catches exceptions unrelated to the args
            except Exception as retard:
                given = eval('len(inspect.signature(a.' + cmd + ').parameters)')
                if nat:
                    given -= 3
                msg = 'This function requires ' + str(given) + ' parameters.\nYou provided ' + str(len(args)) + '.'
                await client.send_message(message.channel, msg)
                print(retard)

    natives.save()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(config['AUTH']['email'], config['AUTH']['pass'])
