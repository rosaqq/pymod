import discord
import sys
import os
import configparser
from types import FunctionType
import gvar
import inspect

config = configparser.ConfigParser()
config.read("pymod.ini")

client = discord.Client()

# join server derp code, commented out for faster boot
'''
if input('Configure?(y/n)') == 'y':
    if input('Join a new server?(y/n)') == 'y':
        invCode = input('Paste invite URL or code here: ')
        client.accept_invite(invCode)
print('Connecting to discord servers...')
'''

gvar.load()

if 'allowed_channels' not in gvar.pyvars:
    gvar.pyvars = {'allowed_channels': []}


# module loader
# ----------------------------------------------------------------------------------------------------------------------


def load_modules():
    gvar.pyvars['class_list'] = []
    gvar.pyvars['cmd_list'] = []
    gvar.pyvars['cmd_dict'] = {}
    mods = os.listdir('mods')
    for j in mods:
        if j.endswith('.py'):
            gvar.pyvars['class_list'].append(str(j)[0:-3])

    sys.path.append('mods')
    for i in gvar.pyvars['class_list']:
        exec("globals()['" + i + "'] = __import__('" + i + "')." + i)

    for v in gvar.pyvars['class_list']:
        class_cmd_list = [x for x, y in eval(v + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]
        gvar.pyvars['cmd_dict'][v] = class_cmd_list
        for w in class_cmd_list:
            gvar.pyvars['cmd_list'].append(w)
    print(gvar.pyvars)


# ----------------------------------------------------------------------------------------------------------------------

load_modules()


@client.event
async def on_message(message):

    if message.content == 'py come':
        gvar.pyvars['allowed_channels'].append(message.channel.id)
        await client.send_message(message.channel, "channel enabled")
    elif message.content == 'py leave':
        gvar.pyvars['allowed_channels'].remove(message.channel.id)
        await client.send_message(message.channel, "channel disabled")

    elif message.channel.id in gvar.pyvars['allowed_channels']:

        if message.content.startswith('py help'):
            helpmsg = 'Available commands are: ```\n' + '\n'.join(gvar.pyvars['cmd_list']) + '```\nUse $x in ' \
                                                                                             'the command to pass ' \
                                                                                             'parameter x to ' \
                                                                                             'a function that ' \
                                                                                             'requires it.'
            await client.send_message(message.channel, helpmsg)
        else:

            cmd_args = message.content.split()
            args = [x for x in cmd_args if '$' in x]
            for asd in args:
                args[args.index(asd)] = args[args.index(asd)].replace('$', '')
            cmd = '_'.join([y for y in cmd_args if '$' not in y])
            for key in gvar.pyvars['cmd_dict']:
                if cmd in gvar.pyvars['cmd_dict'][key]:
                    exec('a = ' + key + '(client, message)')
                    try:
                        await eval('a.' + cmd + '(*args)')
                    except TypeError as error:
                        msg = 'This function requires ' + str(eval('len(inspect.signature(a.' + cmd + ').parameters)'))\
                              + ' parameters.\nYou provided ' + str(len(args)) + '.'
                        await client.send_message(message.channel, msg)
                        print(error)

    gvar.save()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(config['AUTH']['email'], config['AUTH']['pass'])
