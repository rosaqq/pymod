import pickle


class PickleMod:

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_pickle(self, svar, file):
        with open(file + '.pickle', 'wb') as notes:
            exec('pickle.dump(' + svar + ', notes)')
            notes.close()
            print('pickled ' + svar)

    async def py_loadpickle(self, file, lvar):
        try:
            with open(file + '.pickle', 'rb') as notes:
                exec(lvar + ' = pickle.load(notes)')
                notes.close()
            exec('print(' + lvar + ')')
        except IOError:
            await self.client.send_message(self.message.channel, 'No such file.')

