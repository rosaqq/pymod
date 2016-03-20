import discord
import sys
import os
import configparser
from types import FunctionType
import inspect
import logging as very_essential_func_totally_not_logs

# for erm... required init stuff... yes, python mandatory stuff that's it!
# ----------------------------------------------------------------------------------------------------------------------
import time

year, month, day, hour, minute, a, b, c, d = time.localtime(time.time())
platypus = str(year) + 'y' + str(month) + 'm' + str(day) + 'd' + str(hour) + str(minute) + 'h'

erm_I_can_explain_it_is_not_what_you_think = very_essential_func_totally_not_logs.getLogger('discord')
erm_I_can_explain_it_is_not_what_you_think.setLevel(very_essential_func_totally_not_logs.DEBUG)
handler = very_essential_func_totally_not_logs.FileHandler(filename=platypus+'.log', encoding='utf-8', mode='w')
handler.setFormatter(very_essential_func_totally_not_logs.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
erm_I_can_explain_it_is_not_what_you_think.addHandler(handler)
# ----------------------------------------------------------------------------------------------------------------------


# natives loader
# ----------------------------------------------------------------------------------------------------------------------
def load_natives():
    exec("globals()['natives'] = __import__('natives')")
    bot_vars['natives'] = {}
    native_classes = [x for x, y in natives.__dict__.items() if 'Pyc' in x]
    for i in native_classes:
        funcs = [x for x, y in eval('natives.' + i + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]
        bot_vars['natives'][i] = funcs


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
            funcs = [x for x, y in eval(i + '.__dict__.items()') if type(y) == FunctionType and 'py_' in x]
            bot_vars['cmd_dict'][i] = funcs


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
    helplist = {}

    if cmd == 'py_come' or cmd == 'py_leave' or message.channel.id in bot_vars['allowed_channels']:
        try:
            user_rank = bot_vars['ranks'][message.author.id]
        except KeyError:
            user_rank = 0

        try:
            # check if cmd in natives
            for key in bot_vars['natives']:
                if cmd in bot_vars['natives'][key]:
                    if user_rank >= eval('natives.' + key + '.rank'):
                        exec('a = natives.' + key + '(client, message)')
                        await eval('a.' + cmd + '(*args)')
                    else:
                        await client.send_message(message.channel, 'permission denied')
                elif cmd == 'py_help':
                    helpcmd = True
                    if user_rank >= eval('natives.' + key + '.rank'):
                        for func in bot_vars['natives'][key]:
                                helplist[func] = eval('natives.' + key + '.help_dict[func]')
            # check in modules
            for key in bot_vars['cmd_dict']:
                if cmd in bot_vars['cmd_dict'][key]:
                    if user_rank >= eval(key + '.rank'):
                        exec('a = ' + key + '(client, message)')
                        await eval('a.' + cmd + '(*args)')
                    else:
                        await client.send_message(message.channel, 'permission denied')
                elif cmd == 'py_help':
                    helpcmd = True
                    if user_rank >= eval(key + '.rank'):
                        for func in bot_vars['cmd_dict'][key]:
                            helplist[func] = helplist[func] = eval(key + '.help_dict[func]')
            if helpcmd:
                helpmsg = []
                for func in helplist:
                    helpmsg.append(func + ': ' + helplist[func])
                msg = 'Available commands are: ```\n' + '\n'.join(helpmsg) + '```\nUse $x in the command to pass ' \
                                                                                 'parameter x to a function that' \
                                                                                 ' requires it.\n( _ represents a ' \
                                                                                 'space and "py" should be replaced ' \
                                                                                 'by the current callsign)'
                await client.send_message(message.author, msg)

        except Exception as retard:
            msg = 'Something went wrong:\n' + str(retard)
            await client.send_message(message.channel, msg)

    natives.save()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(config['AUTH']['email'], config['AUTH']['pass'])
