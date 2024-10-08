import argparse

argparser = False


def getParser(isPiped=False):
    global argparser
    if argparser:
        return argparser

    argparser = argparse.ArgumentParser(
        description='Interpreter for the byhand language')
    argparser.add_argument('-c', '--config-file', action='append',
                           dest='configPath', type=str,
                           help='the path to the config file')
    argparser.add_argument('-r',  dest='repl', action='store_const',
                           const=True, default=False,
                           help='Use -r if you want to launch the repl')
    if not isPiped:
        argparser.add_argument('script', metavar='script',
                               type=str, nargs='?',
                               help='the path to the script')
    argparser.add_argument('config',  metavar='config', type=str, nargs='?',
                           help='the root key to the config if needed')
    return argparser
