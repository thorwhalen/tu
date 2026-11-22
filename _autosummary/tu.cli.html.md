# tu.cli

Command-line interface for tu.

### Functions

| [`complete_cli`](#tu.cli.complete_cli)(args)           | Handle the --complete command (for shell completion).       |
|-------------------------------------------------------------------------------|-------------------------------------------------------------|
| [`complete_flags_cli`](#tu.cli.complete_flags_cli)(args)     | Handle the --complete-flags command (for shell completion). |
| [`completion_script_cli`](#tu.cli.completion_script_cli)(args)  | Handle the --completion-script command.                     |
| [`create_parser`](#tu.cli.create_parser)()              | Create the argument parser for tu CLI.                      |
| [`export_registry_cli`](#tu.cli.export_registry_cli)(args)    | Handle the --export command.                                |
| [`history_cli`](#tu.cli.history_cli)(args)            | Handle the --history command.                               |
| [`import_registry_cli`](#tu.cli.import_registry_cli)(args)    | Handle the --import command.                                |
| [`install_completion_cli`](#tu.cli.install_completion_cli)(args) | Handle the --install-completion command.                    |
| [`list_commands_cli`](#tu.cli.list_commands_cli)(args)      | Handle the --list command.                                  |
| [`main`](#tu.cli.main)([argv])                 | Main entry point for tu CLI.                                |
| [`print_error`](#tu.cli.print_error)(message)         | Print an error message to stderr.                           |
| [`register_command_cli`](#tu.cli.register_command_cli)(args)   | Handle the --register command.                              |
| [`rename_command_cli`](#tu.cli.rename_command_cli)(args)     | Handle the --rename command.                                |
| [`run_command_cli`](#tu.cli.run_command_cli)(args)        | Handle running a command.                                   |
| [`show_command_cli`](#tu.cli.show_command_cli)(args)       | Handle the --show command.                                  |
| [`stats_cli`](#tu.cli.stats_cli)(args)              | Handle the --stats command.                                 |
| [`unregister_command_cli`](#tu.cli.unregister_command_cli)(args) | Handle the --unregister command.                            |
| [`validate_cli`](#tu.cli.validate_cli)(args)           | Handle the --validate command.                              |

### tu.cli.complete_cli(args)

Handle the –complete command (for shell completion).

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.complete_flags_cli(args)

Handle the –complete-flags command (for shell completion).

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.completion_script_cli(args)

Handle the –completion-script command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.create_parser()

Create the argument parser for tu CLI.

* **Return type:**
  [`ArgumentParser`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)

### tu.cli.export_registry_cli(args)

Handle the –export command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.history_cli(args)

Handle the –history command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.import_registry_cli(args)

Handle the –import command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.install_completion_cli(args)

Handle the –install-completion command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.list_commands_cli(args)

Handle the –list command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.main(argv=None)

Main entry point for tu CLI.

* **Parameters:**
  **argv** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Command-line arguments (defaults to sys.argv[1:]).
* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)
* **Returns:**
  Exit code.

### tu.cli.print_error(message)

Print an error message to stderr.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.cli.register_command_cli(args)

Handle the –register command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.rename_command_cli(args)

Handle the –rename command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.run_command_cli(args)

Handle running a command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.show_command_cli(args)

Handle the –show command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.stats_cli(args)

Handle the –stats command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.unregister_command_cli(args)

Handle the –unregister command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### tu.cli.validate_cli(args)

Handle the –validate command.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)
