### This is a helper library to load blender datagen configs into memory.
### Here is a collection of parameters supported:

import json

def loadConfig(filename, mode='r'):
    with open(filename, mode) as filep:
        data = json.load(filep)
        return data[0]