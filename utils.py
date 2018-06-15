import os, pickle

def touchdir(path, with_name=False):
    if with_name:
        x = path[::-1].find('/')
        if x == -1:
            return True
        path = path[:-x]

    if os.path.isdir(path):
        return False
    os.makedirs(path)
    return True

class Cache(object):
    def __init__(self, path):
        self.path = path
        touchdir(path)

    def save(self, data, name):
        name = os.path.join(self.path, name)
        touchdir(name, True)
        with open(name, 'wb') as f:
            pickle.dump(data, f)

    def bin_save(self, data, name):
        name = os.path.join(self.path, name)
        touchdir(name, True)
        with open(name, 'wb') as f:
            f.write(data)

    def str_save(self, data, name):
        name = os.path.join(self.path, name)
        touchdir(name, True)
        with open(name, 'w') as f:
            f.write(data)

    def load(self, name):
        file_path = os.path.join(self.path, name)
        if not os.path.isfile(file_path):
            return None
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    def bin_load(self, name):
        file_path = os.path.join(self.path, name)
        if not os.path.isfile(file_path):
            return None
        with open(file_path, 'rb') as f:
            return f.read()

    def str_load(self, name):
        file_path = os.path.join(self.path, name)
        if not os.path.isfile(file_path):
            return None
        with open(file_path, 'r') as f:
            return f.read()
