# Byhand :hand:

- [Byhand:hand:](#byhandhand)
- [Introduction](#introduction)
- [Status](#status)
- [Installation](#installation)
  - [Shiv package (recommended)](#shiv-package-recommended)
  - [With pip:](#with-pip)
- [Syntax](#syntax)
- [Preprocessor](#preprocessor)
- [Build](#build)

# Introduction

Byhand :hand: is an interpreted minilanguage written in Python that enables you to
specify processes that requires some manual (non automated) tasks. These tasks can
gradually evolve into automated tasks as people write
scripts to automate specific steps. This allows you to start with a list of manual tasks
defined in natural language and eventually develop them into fully automated scripts.

# Status

 **Experimental** - This is a proof-of-concept prototype. While functional and used
by some colleagues, it is not polished and intended for production issues.

# Installation

## Shiv package (recommended)

It only requires python3 installed on your system

Download the latest shiv package from https://github.com/jjtorroglosa/byhand/releases
(generated with [shiv](https://shiv.readthedocs.io/en/latest/))

## With pip:

`pip3 install git+ssh://git@github.com/jjtorroglosa/byhand`

# Syntax

It has a very simple syntax. Each line contains a command with this syntax: `<command> the command definition`. The commands are:

- `M A manual task`: This is a manual task written in natural language. It waits for the user to press enter when he has completed the task.
- `? The question to the user >output_variable`. E.g. `? Please provide some input`: When executed, it prints "Please provide some input" and stores the user input in $output_variable. That variable can be used then in other commands, for example: `M The user entered $output_variable`.
  - You can specify a list of supported answers this way: `? Any question [answer1/answer2] >output_variable`. `answer1` and `answer2` can be any alphanumeric word.
- `$ command`: It executes command in a shell. It can also be an interactive command like `ssh`, `vim`, etc. An output variable can be provided to store the command output: `$ echo hola >output_variable`
- `O https://any.url`. It opens `https://any.url` in the browser.
- `P Some text`: Just print some text without waiting for any user input.
- `# A comment`: You can add comments to the script.

# Preprocessor

Each script is preprocessed with jinja2 template engine, so you can use any of its features.

You can pass arguments to specify yaml files to read config from, and the config is accessible by the preprocessor. If no config files arguments are passed, the preprocessor looks for ./config.yaml and ./configs/config.yaml by default.

E.g. Given this script:

```
$ cat config.bh
#!/usr/bin/env byhand
P Config read with preprocessor: {{serviceConfig.services.UserService.http_location}}
```

If we execute it with a serviceConfig.yaml file from unified_config:
```
$ ./config.bh -c ~/src/unified_config/environment/novum/base/common/serviceConfig.yaml
Config read with preprocessor: http://user-service
```

# Build

Run:
```make bin```
