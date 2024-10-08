
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
LIGHT_BLUE = '\033[96m'
ENDC = '\033[0m'


def blue(str):
    return color(BLUE, str)


def lightblue(str):
    return color(LIGHT_BLUE, str)


def green(str):
    return color(GREEN, str)


def red(str):
    return color(RED, str)


def color(color, string):
    return color + string + ENDC
