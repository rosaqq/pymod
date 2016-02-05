import pickle

pyvars = {}


def save():
    global pyvars
    with open('pyvars.pickle', 'wb') as save_file:
        pickle.dump(pyvars, save_file)
        save_file.close()


def load():
    global pyvars
    try:
        with open('pyvars.pickle', 'rb') as save_file:
            pyvars = pickle.load(save_file)
            save_file.close()
    except IOError:
        save()
