import pickle
import os
import shutil


class PickleMod:
    rank = 100
    help_dict = {'py_pickle': 'save something to file', 'py_loadpickle': 'chat what was saved in the specified file',
                 'py_delpickle': 'trash a pickle'}

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.folder = 'pickles'

    async def py_pickle(self, file, someth):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        with open(self.folder + '/' + file + '.pickle', 'wb') as notes:
            pickle.dump(someth, notes)
            notes.close()
            await self.client.send_message(self.message.channel, 'pickled')

    async def py_loadpickle(self, file):
        try:
            with open(self.folder + '/' + file + '.pickle', 'rb') as notes:
                someth = pickle.load(notes)
                notes.close()
            await self.client.send_message(self.message.channel, someth)
        except IOError:
            await self.client.send_message(self.message.channel, 'No such file.')

    async def py_delpickle(self, file):
        try:
            if file == '\\all':
                shutil.rmtree(self.folder)
                os.makedirs(self.folder)
                await self.client.send_message(self.message.channel, 'all the pickles trashed.')
            else:
                os.remove(self.folder + '/' + file + '.pickle')
                await self.client.send_message(self.message.channel, 'pickle trashed.')
        except IOError:
            await self.client.send_message(self.message.channel, 'No such file.')
