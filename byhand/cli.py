import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def question(message):
    result = input(message + " [Y/n]: ").lower()
    while result not in ["y", "n"] and result:
        result = input(message + " [Y/n]: ")
    return not result.strip() or result == "y"


def debug(message):
    print(message)
