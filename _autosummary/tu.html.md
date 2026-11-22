# tu

tu - Terminal Utils: Quick access to your favorite scripts.

A unified entry point for running scripts and commands with a hierarchical namespace.

### Functions

| [`list_commands`](#tu.list_commands)([pattern, use_layered])           | List all registered commands.               |
|--------------------------------------------------------------------------------------------------|---------------------------------------------|
| [`get_command_info`](#tu.get_command_info)(name[, use_layered])           | Get information about a registered command. |
| [`register_command`](#tu.register_command)(target, \*[, name, type, ...]) | Register a new command.                     |
| [`unregister_command`](#tu.unregister_command)(name)                        | Unregister a command.                       |
| [`rename_command`](#tu.rename_command)(old_name, new_name)              | Rename a command.                           |
| [`run`](#tu.run)(name[, args, capture_output, dry_run, ...]) | Run a command.                              |

### Classes

| [`RegisteredCommand`](#tu.RegisteredCommand)(name, type, target[, ...])      | Represents a registered command in the tu registry.   |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| [`RunResult`](#tu.RunResult)(returncode[, stdout, stderr, duration]) | Result of running a command.                          |
| [`ExecutionPlan`](#tu.ExecutionPlan)(command_type, target[, args, ...])  | Plan for executing a command.                         |
| [`HistoryEntry`](#tu.HistoryEntry)(command_name, args, returncode, ...) | Entry in command execution history.                   |

### Exceptions

| [`TuError`](#tu.TuError)                 | Base exception for all tu errors.                                   |
|--------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`UnknownCommandError`](#tu.UnknownCommandError)     | Raised when a command is not found in the registry.                 |
| [`NameCollisionError`](#tu.NameCollisionError)      | Raised when attempting to register a command with an existing name. |
| [`RegistryCorruptedError`](#tu.RegistryCorruptedError)  | Raised when the registry file is corrupted or invalid.              |
| [`InvalidCommandTypeError`](#tu.InvalidCommandTypeError) | Raised when an invalid command type is specified.                   |
| [`InvalidNameError`](#tu.InvalidNameError)        | Raised when a command name is invalid.                              |
| [`CommandExecutionError`](#tu.CommandExecutionError)   | Raised when a command fails to execute.                             |

### *exception* tu.CommandExecutionError

Bases: [`TuError`](tu.exceptions.html.md#tu.exceptions.TuError)

Raised when a command fails to execute.

### *class* tu.ExecutionPlan(command_type, target, args=list(), cwd=None, env=None, timeout=None, dry_run=False, verbose=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Plan for executing a command.

This represents the execution context and is used by global options
to transform command execution.

#### command_type

Type of command to execute

* **Type:**
  [`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'shell'`, `'python_module'`, `'python_callable'`]

#### target

The target to execute

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### args

Arguments to pass to the command

* **Type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### cwd

Working directory for execution

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### env

Environment variables

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]

#### timeout

Timeout in seconds

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]

#### dry_run

If True, show what would execute without running

* **Type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

#### verbose

If True, show detailed execution information

* **Type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* tu.HistoryEntry(command_name, args, returncode, executed_at, duration, cwd=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Entry in command execution history.

#### command_name

Name of the command that was executed

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### args

Arguments passed to the command

* **Type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### returncode

Exit code from execution

* **Type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

#### executed_at

Timestamp of execution

* **Type:**
  [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)

#### duration

Execution duration in seconds

* **Type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

#### cwd

Working directory at execution time

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### *classmethod* from_dict(data)

Create from dictionary during JSON deserialization.

* **Return type:**
  [`HistoryEntry`](tu.models.html.md#tu.models.HistoryEntry)

#### to_dict()

Convert to dictionary for JSON serialization.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *exception* tu.InvalidCommandTypeError

Bases: [`TuError`](tu.exceptions.html.md#tu.exceptions.TuError)

Raised when an invalid command type is specified.

### *exception* tu.InvalidNameError

Bases: [`TuError`](tu.exceptions.html.md#tu.exceptions.TuError)

Raised when a command name is invalid.

### *exception* tu.NameCollisionError

Bases: [`TuError`](tu.exceptions.html.md#tu.exceptions.TuError)

Raised when attempting to register a command with an existing name.

### *class* tu.RegisteredCommand(name, type, target, description=None, tags=list(), created_at=datetime.now(), updated_at=datetime.now(), aliases=list(), depends_on=list(), env=dict(), timeout=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Represents a registered command in the tu registry.

#### name

Fully qualified name (FQN) of the command

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### type

Type of command (shell, python_module, python_callable)

* **Type:**
  [`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'shell'`, `'python_module'`, `'python_callable'`]

#### target

The actual target to execute (command, module path, callable)

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### description

Optional description of the command

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### tags

List of tags for categorization

* **Type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### created_at

Timestamp when the command was registered

* **Type:**
  [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)

#### updated_at

Timestamp when the command was last updated

* **Type:**
  [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)

#### aliases

List of alternative names for this command

* **Type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### depends_on

List of command names that must run before this one

* **Type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### env

Environment variables to set when running this command

* **Type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### timeout

Timeout in seconds for command execution

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]

#### *classmethod* from_dict(name, data)

Create from dictionary during JSON deserialization.

* **Return type:**
  [`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)

#### to_dict()

Convert to dictionary for JSON serialization.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *exception* tu.RegistryCorruptedError

Bases: [`TuError`](tu.exceptions.html.md#tu.exceptions.TuError)

Raised when the registry file is corrupted or invalid.

### *class* tu.RunResult(returncode, stdout=None, stderr=None, duration=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Result of running a command.

#### returncode

Exit code from the command

* **Type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

#### stdout

Captured stdout (if requested)

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### stderr

Captured stderr (if requested)

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### duration

Execution duration in seconds

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`float`](https://docs.python.org/3/builtins/functions.html#float)]

### *exception* tu.TuError

Bases: [`Exception`](https://docs.python.org/3/builtins/exceptions.html#Exception)

Base exception for all tu errors.

### *exception* tu.UnknownCommandError

Bases: [`TuError`](tu.exceptions.html.md#tu.exceptions.TuError)

Raised when a command is not found in the registry.

### tu.get_command_info(name, use_layered=True)

Get information about a registered command.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name or alias.
  * **use_layered** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, search project-local registry too.
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  RegisteredCommand if found, None otherwise.

### tu.list_commands(pattern=None, use_layered=True)

List all registered commands.

* **Parameters:**
  * **pattern** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional pattern to filter command names (substring match).
  * **use_layered** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, include project-local commands.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  List of RegisteredCommand objects.

### tu.register_command(target, , name=None, type=None, description=None, tags=None, aliases=None, depends_on=None, env=None, timeout=None, allow_dot_name=False)

Register a new command.

* **Parameters:**
  * **target** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target to execute (command, module, callable).
  * **name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Command name (FQN). If None, inferred from target.
  * **type** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Command type (shell, python_module, python_callable). If None, inferred.
  * **description** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional description.
  * **tags** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Optional list of tags.
  * **aliases** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Optional list of alternative names.
  * **depends_on** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Optional list of commands this depends on.
  * **env** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Optional environment variables to set.
  * **timeout** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Optional timeout in seconds.
  * **allow_dot_name** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Allow registering names with dots without confirmation.
* **Return type:**
  [`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)
* **Returns:**
  The registered RegisteredCommand.
* **Raises:**
  * [**NameCollisionError**](#tu.NameCollisionError) – If the name already exists.
  * [**InvalidNameError**](#tu.InvalidNameError) – If the name is invalid.

### tu.rename_command(old_name, new_name)

Rename a command.

* **Parameters:**
  * **old_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Current name of the command.
  * **new_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – New name for the command.
* **Raises:**
  * [**UnknownCommandError**](#tu.UnknownCommandError) – If the old command doesn’t exist.
  * [**NameCollisionError**](#tu.NameCollisionError) – If the new name already exists.
  * [**InvalidNameError**](#tu.InvalidNameError) – If the new name is invalid.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.run(name, args=None, , capture_output=False, dry_run=False, verbose=False, timeout_override=None, log_output=False, log_dir=None, track_history=True)

Run a command.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name to run.
  * **args** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Arguments to pass to the command.
  * **capture_output** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to capture stdout/stderr.
  * **dry_run** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show what would execute without running.
  * **verbose** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show detailed execution information.
  * **timeout_override** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Override the command’s timeout setting.
  * **log_output** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, write output to log file.
  * **log_dir** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional directory for log files.
  * **track_history** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, add to command history.
* **Return type:**
  [`RunResult`](tu.models.html.md#tu.models.RunResult)
* **Returns:**
  RunResult with execution results.
* **Raises:**
  * [**UnknownCommandError**](#tu.UnknownCommandError) – If the command is not found and not a dotted name.
  * [**CommandExecutionError**](#tu.CommandExecutionError) – If execution fails.

### tu.unregister_command(name)

Unregister a command.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name to unregister.
* **Raises:**
  [**UnknownCommandError**](#tu.UnknownCommandError) – If the command doesn’t exist.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### Modules

| [`api`](tu.api.html.md#module-tu.api)               | Python API for tu package.            |
|----------------------------------------------------------------------------------|---------------------------------------|
| [`cli`](tu.cli.html.md#module-tu.cli)               | Command-line interface for tu.        |
| [`completion`](tu.completion.html.md#module-tu.completion) | Shell completion support for tu.      |
| [`exceptions`](tu.exceptions.html.md#module-tu.exceptions) | Custom exceptions for the tu package. |
| [`execute`](tu.execute.html.md#module-tu.execute)       | Command execution for tu.             |
| [`history`](tu.history.html.md#module-tu.history)       | Command execution history tracking.   |
| [`log`](tu.log.html.md#module-tu.log)               | Command output logging for tu.        |
| [`models`](tu.models.html.md#module-tu.models)         | Data models for the tu package.       |
| [`options`](tu.options.html.md#module-tu.options)       | Global options framework for tu.      |
| [`registry`](tu.registry.html.md#module-tu.registry)     | Registry management for tu commands.  |
| [`repl`](tu.repl.html.md#module-tu.repl)             | Interactive REPL mode for tu.         |
| [`resolve`](tu.resolve.html.md#module-tu.resolve)       | Command name resolution for tu.       |
| [`utils`](tu.utils.html.md#module-tu.utils)           | Utility functions for tu.             |
