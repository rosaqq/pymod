import discord
import sys
import os
import configparser
from types import FunctionType
import inspect
import colorlog
import logging
import time
from colored import fg, bg, attr

# Console logging
# ----------------------------------------------------------------------------------------------------------------------

# logger = colorlog.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# # Warning: there's a massive dump of shit in the console when it starts up
# formatter = colorlog.ColoredFormatter(
#     "%(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
#     log_colors = {
#         'DEBUG': 'blue',
#         'INFO': 'green',
#         'WARNING': 'yellow',
#         'ERROR': 'red',
#         'CRITICAL': 'bold_red, bg_white',
#     },
#     secondary_log_colors={
#         'message': {
#             'DEBUG': 'white',
#             'INFO': 'white',
#             'WARNING': 'yellow',
#             'ERROR':    'red',
#             'CRITICAL': 'red'
#         }
#     })
# handler.setFormatter(formatter)
# logger.addHandler(handler)


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
# print('bot_vars pre-set to: ' + str(bot_vars))


@client.event
async def on_message(message):
    if "ako pls" in message.content.lower():
        # print("%s" + time.strftime("%Y-%m-%d %H:%M:%S") + " AKOPLS: " + message.author.name + "| akopls incremented%s" % (fg(2), attr(0)))
        try:
            bot_vars['akopls'] += 1
        except KeyError:
            bot_vars['akopls'] = 1

    if "00 uptime" in message.content.lower():
        # Kinda hijacked this because I couldn't figure out a way to get bot_vars from a mod file, lol
        await client.send_message(message.channel, "Uptime: {0:.2f} seconds".format((time.time() - bot_vars['start_time'])))
    cmd, args = natives.parse(message)
    helpcmd = False
    helplist = {}

    if cmd == 'ratelimit' and (cmd == 'py_come' or message.channel.id in bot_vars['allowed_channels']):
         print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " RATELIMIT: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))

    if cmd == 'py_come' or cmd == 'py_leave' or message.channel.id in bot_vars['allowed_channels']:
        try:
            user_rank = bot_vars['ranks'][message.author.id]
        except KeyError:
            user_rank = 0

        for command in bot_vars['custom_cmds']:
            #idk what I'm doing anymore
            if "00 " + command == message.content.lower() and user_rank >= 0:
                await client.send_message(message.channel, bot_vars['custom_cmds'][command])


        # if False:
        #     pass
        #
        # else:
        try:
            # check if cmd in natives
            for key in bot_vars['natives']:
                if cmd in bot_vars['natives'][key]:
                    if user_rank >= eval('natives.' + key + '.rank'):
                        exec('a = natives.' + key + '(client, message)')
                        print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " NATIVE_SUCCESS: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))
                        await eval('a.' + cmd + '(*args)')
                        # print("%s" % (fg(2)) + time.strftime("%Y-%m-%d %H:%M:%S") + " NATIVE_SUCCESS: " + message.author.name + "| command executed: " + cmd + " with args: " + " ".join(args) + "%s" % (attr(0)))

                    else:
                        print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " NATIVE_DENY: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))
                        await client.send_message(message.channel, 'permission denied')
                        # print("%s" % (fg(1)) + time.strftime("%Y-%m-%d %H:%M:%S") + " NATIVE_DENY: " + message.author.name + "| command NOT executed: " + cmd + " with args: " + " ".join(args) + "%s" % (attr(0)))

                elif cmd == 'py_help':
                    print("%s" % (fg(2)) + time.strftime("%Y-%m-%d %H:%M:%S") + " HELP: " + message.author.name + "| command executed: " + cmd + " with args: " + " ".join(args) + "%s" % (attr(0)))
                    helpcmd = True
                    if user_rank >= eval('natives.' + key + '.rank'):
                        for func in bot_vars['natives'][key]:
                            helplist[func] = eval('natives.' + key + '.help_dict[func]')
                            helplist[func] += "      rank: " + str(eval('natives.' + key + '.rank'))
            # check in modules
            for key in bot_vars['cmd_dict']:
                if cmd in bot_vars['cmd_dict'][key]:
                    if user_rank >= eval(key + '.rank'):
                        exec('a = ' + key + '(client, message)')
                        print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " MOD_SUCCESS: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))
                        await eval('a.' + cmd + '(*args)')
                        # print("%s" % (fg(2)) + time.strftime("%Y-%m-%d %H:%M:%S") + " MOD_SUCCESS: " + message.author.name + "| command executed: " + cmd + " with args: " + " ".join(args) + "%s" % (attr(0)))

                    else:
                        print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " MOD_DENY: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))
                        await client.send_message(message.channel, 'permission denied')
                        # print("%s" % (fg(1)) + time.strftime("%Y-%m-%d %H:%M:%S") + " MOD_DENY: " + message.author.name + "| command NOT executed: " + cmd + " with args: " + " ".join(args) + "%s" % (attr(0)))

                elif cmd == 'py_help':
                    helpcmd = True
                    if user_rank >= eval(key + '.rank'):
                        for func in bot_vars['cmd_dict'][key]:
                            helplist[func] = eval(key + '.help_dict[func]')
                            helplist[func] += "      rank: " + str(eval(key + '.rank'))

            if helpcmd:
                helpmsg = []
                for func in helplist:
                    helpmsg.append(func.replace("py", "00", 1) + ': ' + helplist[func])
                msg = 'Available commands are: \n' + '\n'.join(sorted(helpmsg))
                await safe_send(message.author, msg)
                await client.send_message(message.channel, "<@" + message.author.id + "> Check your DMs for help")

        except Exception as e:
            try:
                msg = str(e.__type__) + ": " + str(e)
                print("{}{:>20}{:<10}{}{:<15}{}{}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " EXCEPTION: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content, "| ErrorMsg: ", msg))
                await client.send_message(message.channel, msg)
            except AttributeError:
                msg = "Exception: " + str(e)
                print("{}{:>20}{:<10}{}{:<15}{}{}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " EXCEPTION: ",
                                                              message.author.name[:10], "| Channel: ", message.channel.name[:15],
                                                              "| Msg: ", message.content, "| ErrorMsg: ", msg))
                await client.send_message(message.channel, msg)

    if message.channel.id in bot_vars['allowed_channels'] and not message.content.lower().startswith("00") and message.author != client.user:
        print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " LISTEN_MSG: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))
    elif not (cmd == 'py_come' or cmd == 'py_leave' or message.channel.id in bot_vars['allowed_channels']) and message.author != client.user:
        print("{}{:>20}{:<10}{}{:<15}{}{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), " NON_LISTEN_MSG: ", message.author.name[:10], "| Channel: ", message.channel.name[:15], "| Msg: ", message.content))

    natives.save()


def check(itera, s):
    """Idk why I made this"""
    for i in itera:
        if i in s:
            return True
    return False


async def safe_send(channel, message):
    if len(message) < 1990:
        await client.send_message(channel, message)
    else:
        while len(message) > 1990 and message.rfind("\n", 0, 1990) != -1:
            inx = message.rfind("\n", 0, 1990)
            await client.send_message(channel, message[:inx])
            message = message[inx:]
        await client.send_message(channel, message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    bot_vars['start_time'] = time.time()



client.run(config['AUTH']['token'])
