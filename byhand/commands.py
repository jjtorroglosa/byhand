import subprocess
import webbrowser
from .cli import eprint, question
import shlex
import sys
import re
from .colors import blue, red, green
from .errors import RuntimeException, ParserException
from .args import getParser
import byhand.memory as Memory
import clipboard
import os

VARIABLE_READ_PREG = re.compile(r'([^\\]\$([\.\w_-]+))')
VARIABLE_SAVE_PREG = re.compile(r'([^\\]\>(\w+))')
RESPONSES = re.compile(r'(\[(\w+)(?:\/(\w+))+\])')
COMMAND_MODE = "bash"


class Command:
    def create(command, line, lineNumber=0):
        func = COMMANDS.get(command, "Not found")

        if func == "Not found":
            eprint("Syntax error. Unknown command found at line: "
                   + str(lineNumber))
            eprint(">>> " + line)
            exit(1)

        return func(line, lineNumber)

    def __init__(self, line, lineNumber):
        self.line = line
        self.lineNumber = lineNumber

    def run(self):
        self.line = Command._interpolate(self.line, self.lineNumber)
        self._preExecutionParsing()
        self._exec()

    def _preExecutionParsing(self):
        pass

    def _exec(self):
        pass

    def _interpolate(string, lineNumber):
        def sub(matches):
            varName = matches.groups()[1]
            value = Memory.get(varName)
            if not value:
                raise RuntimeException(
                    message="Undefined variable {} found at line {}:\n{}"
                    .format(blue("$"+varName), lineNumber, ">>> "+red(string)))

            return " " + value

        return VARIABLE_READ_PREG.sub(sub, string).replace('\\$', '$')

    def _getOutputVariable(self, mandatory=True):
        def _removeOutputVariable(match):
            result = match.string[0:match.start(
                0)] + match.string[match.end(0):len(match.string)]
            return result.strip()
        iter = VARIABLE_SAVE_PREG.finditer(self.line)
        matches = [i for i in iter]
        if len(matches) == 1:
            match = matches[0]
            self.line = _removeOutputVariable(match)
            self.variableName = match.groups(0)[1]
        elif mandatory:
            raise ParserException(
                message="Error while parsing line: " +
                "%s. One and only one output variable must be defined\n%s"
                % (self.lineNumber, ">>> "+red(self.line)))
        else:
            self.variableName = False


class ConfigRequiredCommand(Command):
    def _exec(self):
        from .interpreter import configRead
        if not configRead:
            eprint(
                "Error: Config required but not provided. " +
                "Please execute the script with the config as argument")
            getParser().print_help()
            exit(1)


class Manual(Command):
    def _exec(self):
        print(input("✋ " + green(self.line)+" [enter] "), end="")


class Print(Command):
    def _exec(self):
        print(self.line)


class Shell(Command):
    def _preExecutionParsing(self):
        self._getOutputVariable(mandatory=False)

    def _exec(self):
        print("💻 " + blue("$ " + self.line))
        try:
            stdout = subprocess.PIPE if self.variableName else sys.stdout
            if COMMAND_MODE == "bash":
                process = subprocess.Popen(
                    ["bash", "-c", self.line], stderr=stdout, stdin=sys.stdin,
                    stdout=stdout, env=os.environ.copy())
            elif COMMAND_MODE == "shell_true":
                process = subprocess.Popen(shlex.split(
                    self.line), shell=True, stderr=stdout, stdin=sys.stdin,
                    stdout=stdout, env=os.environ.copy())
            else:
                raise RuntimeException(
                    "Error: Can't run scripts. Unknown COMMAND_MODE found")

            exitStatus = process.wait()
            if self.variableName:
                process.stdout.flush()
                output = process.stdout.read().decode().strip()
                print(output)
                Memory.memory[self.variableName] = output
            print("💻 " + blue("Script finished. Exit status was: %d"
                  % exitStatus))
        except OSError as e:
            print(red("💻 Error executing script\n>>> %s" % str(e)))
        except Exception as e:
            raise e


class OpenBrowser(Command):
    def _exec(self):
        if question("🌍 " + blue("Open "+self.line+"?")):
            webbrowser.open(self.line)


class Question(Command):
    def _preExecutionParsing(self):
        self._getOptions()
        self._getOutputVariable()

    def _getOptions(self):
        try:
            self.options = next(RESPONSES.finditer(self.line)).groups(0)[1:]
        except StopIteration:
            self.options = []

    def _exec(self):
        def ask():
            return input("❓ %s: " % self.line)
        result = ask()
        while len(self.options) > 0 and result not in self.options:
            print("The only valid answers are %s" % ", ".join(self.options))
            result = ask()
        Memory.memory[self.variableName] = result


class Copy(Command):
    def _exec(self):
        clipboard.copy(self.line)
        print("📋 Copied to clipbard: {}".format(self.line))


class Paste(Command):
    def _exec(self):
        Memory.memory["PASTEBOARD"] = clipboard.paste()


COMMANDS = {
    '.config': ConfigRequiredCommand,
    'M': Manual,
    'P': Print,
    '$': Shell,
    'O': OpenBrowser,
    '?': Question,
    'COPY': Copy}

