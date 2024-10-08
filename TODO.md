ERRORS
[ ] Redirection from a shell to a variable doesn't work properly if the script is interactive. The stdout is not shown.

TESTS CASES
[ ] Interpreter
  [ ] Config path specified by command line
  [ ] Several configs are merged
  [ ] Root key required with .config
  [ ] If no root key, yaml is loaded as is
  [ ] Script from stdin
  [ ] Preprocessor (jinja) is run
  [ ] Several configs are merged
[ ] Commands
    - $
        [ ] env variables work (escaping)
        [ ] variable interpolation works
        [ ] output redirection to a variable work
        [ ] errors are captured
        [ ] exit status is shown
        [ ] a command with a pipe works

NEW FEATURES
[ ] Add $? command: ask the user if he wants to execute a command [y/n] and execute it if affirmative.
[ ] Add colour tags
[ ] REPL
[ ] inline shell scripts
[ ] Scripts dry run
[ ] Capture ctrl+c

[X] use $ for runtime variables
[X] Build distribution
[X] Config is not mandatory
[X] clipboard
