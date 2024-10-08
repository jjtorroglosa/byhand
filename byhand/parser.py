from typing import List
from .commands import Command
import io

def parseScript(iterator) -> List[Command]:
    lineNumber = 0
    parsedCommands = []

    for line in iterator:
        line = line.rstrip()
        lineNumber = lineNumber + 1
        command = parseCommand(lineNumber, line)
        if not command:
            continue
        parsedCommands.append(command)
    return parsedCommands


def parseCommand(lineNumber, line):
    line = line.rstrip().lstrip()
    if not line.strip() or line[0] == "#":
        return False

    command = line.split(' ', 1)[0]
    line = line[len(command)+1:]

    return Command.create(command, line, lineNumber)