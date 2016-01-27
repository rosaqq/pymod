import discord
import sys
import os
import configparser
from types import FunctionType

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

allowed_channels = ['140225706230677504']

# module loader
# ----------------------------------------------------------------------------------------------------------------------


def load_modules():
    class_list = []
    module_list = os.listdir('mods')
    for j in module_list:
        if j.endswith('.py'):
            class_list.append(str(j)[0:-3])
    return class_list

valid_list = load_modules()

sys.path.append('mods')
for i in valid_list:
    c = __import__(i)
    exec(i + " = c." + i)

cmd_dict = {}
for v in valid_list:
    cmd_list = [x for x, y in eval(v + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]
    cmd_dict[v] = cmd_list
# ----------------------------------------------------------------------------------------------------------------------


@client.event
async def on_message(message):

    if message.channel.id in allowed_channels:
        cmd = '_'.join(message.content.split())
        for key in cmd_dict:
            if cmd in cmd_dict[key]:
                print(key)
                print(cmd)
                exec('a = ' + key + '(client, message)')
                await eval('a.' + cmd + '()')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(config['AUTH']['email'], config['AUTH']['pass'])
