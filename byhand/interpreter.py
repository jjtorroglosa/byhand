import os
import sys
from jinja2 import Template
import yaml
from .cli import eprint
from . import parser
import io
import select
from .errors import RuntimeException
from .args import getParser
import byhand.memory as Memory

configRead = False


def main():
    isPiped = select.select([sys.stdin,], [], [], 0.0)[0]
    parser = getParser(isPiped)
    args = parser.parse_args()

    try:
        if isPiped or args.repl:
            script = sys.stdin
            sys.stdin = open("/dev/tty", "r")
            execute(script, args.config, args.configPath)
        else:
            scriptpath = args.script
            if not scriptpath:
                raise RuntimeException("You must provide a script\n%s" % parser
                                       .format_usage().strip())
            with open(scriptpath, "r", encoding="utf-8") as script:
                execute(script, args.config, args.configPath)
    except FileNotFoundError as e:
        eprint(str(e))
    except RuntimeException as e:
        if (str(e)):
            eprint(str(e))
        else:
            raise e


def execute(script, config, configPath):
    read(preprocess(script, config, configPath))


def read(stream):
    parsedCommands = parser.parseScript(stream)
    for i in parsedCommands:
        i.run()


def preprocess(template, config, configPath):
    if not configPath:
        configPath = ["config.yaml", "configs/config.yaml"]

    Memory.memory['config'] = {}
    templateContents = template.read()

    for file in configPath:
        if os.path.isfile(file):
            global configRead
            configRead = True
            if config:
                readConfig = yaml.safe_load(open(file))[config]
            else:
                readConfig = yaml.safe_load(open(file))
            Memory.memory['config'] = {**Memory.memory['config'], **readConfig}

    return io.StringIO(Template(templateContents)
                       .render(Memory.memory['config']))


def contents(filename):
    with open(filename) as f:
        return f.read()
