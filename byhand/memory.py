
memory = {}

def _():
    return memory

def get(path):
    return getArray(memory, path.split('.'))

def getArray(memory, path):
    if path[0] not in memory:
        return None
    if len(path) == 1:
        return memory[path[0]]
    return getArray(memory[path[0]], path[1:])