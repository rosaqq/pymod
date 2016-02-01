import discord
import sys
import os
import configparser
from types import FunctionType
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

allowed_channels = ['140225706230677504', '143055883755192321', '128470036980563968']

# module loader
# ----------------------------------------------------------------------------------------------------------------------


def load_modules():
    global cmd_dict
    global global_cmd_list
    class_list = []
    global_cmd_list = []
    cmd_dict = {}
    module_list = os.listdir('mods')
    for j in module_list:
        if j.endswith('.py'):
            class_list.append(str(j)[0:-3])

    sys.path.append('mods')
    for i in class_list:
        exec("globals()['" + i + "'] = __import__('" + i + "')." + i)

    for v in class_list:
        class_cmd_list = [x for x, y in eval(v + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]
        cmd_dict[v] = class_cmd_list
        for w in class_cmd_list:
            global_cmd_list.append(w)
    print(class_list)
    print(cmd_dict)


# ----------------------------------------------------------------------------------------------------------------------

load_modules()


@client.event
async def on_message(message):

    if message.channel.id in allowed_channels:

        if message.content.startswith('py help'):
            helpmsg = 'Available commands are: ```\n' + '\n'.join(global_cmd_list) + '```\nUse $x in the command ' \
                                                                                     'to pass parameter x to ' \
                                                                                     'a function that requires it'
            await client.send_message(message.channel, helpmsg)
        else:

            cmd_args = message.content.split()
            args = [x for x in cmd_args if '$' in x]
            for asd in args:
                args[args.index(asd)] = args[args.index(asd)].replace('$', '')
            cmd = '_'.join([y for y in cmd_args if '$' not in y])
            for key in cmd_dict:
                if cmd in cmd_dict[key]:
                    exec('a = ' + key + '(client, message)')
                    try:
                        await eval('a.' + cmd + '(*args)')
                    except TypeError:
                        msg = 'This function requires ' + str(eval('len(inspect.signature(a.' + cmd + ').parameters)'))\
                              + ' parameters.\nYou provided ' + str(len(args)) + '.'
                        await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(config['AUTH']['email'], config['AUTH']['pass'])
