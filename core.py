import discord
import pymods

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


@client.event
async def on_message(message):

    cmd_array = [s for s in dir(pymods) if 'py_' in s]
    cmd = '_'.join(message.content.split())

    if message.channel.id in allowed_channels:

        # list commands
        if cmd == 'py_help':
            await client.send_message(message.channel, '```Available commands are:\n' + '\n'.join(cmd_array) + '```')

        # chats the return of any function in the module file
        if cmd in cmd_array:
            await client.send_message(message.channel, eval('pymods.' + cmd + '()'))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('user', 'pass')
