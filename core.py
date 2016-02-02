import discord
import sys
import os
import configparser
from types import FunctionType
import pickle

config = configparser.ConfigParser()
config.read("pymod.ini")

client = discord.Client()

global debug
debug = False

# pickling and stuff
db = {}
try:
    # Opens the saved db dict, will fail when empty so it's excepted with a console log
    with open('pymod.txt', 'rb') as db_dict:
        db = pickle.load(db_dict)
except EOFError:
    print("Either pymod.txt is empty (which is okay), or something else went wrong (which might be less okay).")

# join server derp code, commented out for faster boot

if input('Configure?(y/n)') == 'y':
    if input("Debug? ") == 'y':
        global debug
        debug = True
    if input('Join a new server?(y/n)') == 'y':
        invCode = input('Paste invite URL or code here: ')
        client.accept_invite(invCode)
    if input('Add rank?(y/n)') ==  'y':
        id = input('Paste your id (not name) here: ')
        while True:
            try:
                rank = int(input("What rank would you like this id to be? (0-100)"))
                if rank < 0 or rank > 100:
                    raise ValueError
                break
            except ValueError as e:
                print("Gj you broke it. Here's the error: " + str(e) + " Try again, don't break it this time.")
        if 'ranks' in db:
            db['ranks'][id] = rank
        else:
            db['ranks'] = {id : rank}
        with open('pymod.txt', 'wb') as db_dict:
            # Saves the ranks eveytime a message is received. Easy and probably really inefficant but good enough.
            pickle.dump(db, db_dict)
        if debug:
            print(db)

print('Connecting to discord servers...')


allowed_channels = ['140225706230677504', '143055883755192321', '128470036980563968']

# module loader
# ----------------------------------------------------------------------------------------------------------------------


def load_modules():
    global cmd_dict
    global global_cmd_list
    global rank_dict
    class_list = []
    global_cmd_list = []
    cmd_dict = {}
    rank_dict = {}

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

    for x in class_list:  # Generate rank requirements. Can only be done per module globally, but we can work around it
        rank_dict[x] = eval(x + '.rank')

    if debug:
        print(class_list)
        print(cmd_dict)
        print(rank_dict)


# ----------------------------------------------------------------------------------------------------------------------

load_modules()

@client.event
async def on_message(message):
    global rank_dict

    if message.channel.id in allowed_channels:

        if '_'.join(message.content.split()).lower().startswith("py_help"):
            help_msg = "```"
            for i in rank_dict:
                # if int(i) <= int(ranks[message.author.id]):  # TODO: impliment ranks
                help_msg += eval(i + '.help')
            help_msg += '```\nUse `$x` in the command to pass parameter `x` to a function that requires it'
            await client.send_message(message.channel, help_msg)
        elif '_'.join(message.content.split()).lower().startswith("py_rank"):
            pass

        elif '_'.join(message.content.split()).lower().startswith("py_save_enable"):
            pass

        elif '_'.join(message.content.split()).lower().startswith("py_save_disable"):
            pass

        elif '_'.join(message.content.split()).lower().startswith("py_save"):
            pass

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
