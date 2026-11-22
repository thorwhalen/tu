# tu.api

Python API for tu package.

### Functions

| [`get_command_info`](#tu.api.get_command_info)(name[, use_layered])           | Get information about a registered command.   |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------|
| [`list_commands`](#tu.api.list_commands)([pattern, use_layered])           | List all registered commands.                 |
| [`register_command`](#tu.api.register_command)(target, \*[, name, type, ...]) | Register a new command.                       |
| [`rename_command`](#tu.api.rename_command)(old_name, new_name)              | Rename a command.                             |
| [`run`](#tu.api.run)(name[, args, capture_output, dry_run, ...]) | Run a command.                                |
| [`unregister_command`](#tu.api.unregister_command)(name)                        | Unregister a command.                         |

### tu.api.get_command_info(name, use_layered=True)

Get information about a registered command.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name or alias.
  * **use_layered** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, search project-local registry too.
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  RegisteredCommand if found, None otherwise.

### tu.api.list_commands(pattern=None, use_layered=True)

List all registered commands.

* **Parameters:**
  * **pattern** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional pattern to filter command names (substring match).
  * **use_layered** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, include project-local commands.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  List of RegisteredCommand objects.

### tu.api.register_command(target, , name=None, type=None, description=None, tags=None, aliases=None, depends_on=None, env=None, timeout=None, allow_dot_name=False)

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
  * [**NameCollisionError**](tu.html.md#tu.NameCollisionError) – If the name already exists.
  * [**InvalidNameError**](tu.html.md#tu.InvalidNameError) – If the name is invalid.

### tu.api.rename_command(old_name, new_name)

Rename a command.

* **Parameters:**
  * **old_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Current name of the command.
  * **new_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – New name for the command.
* **Raises:**
  * [**UnknownCommandError**](tu.html.md#tu.UnknownCommandError) – If the old command doesn’t exist.
  * [**NameCollisionError**](tu.html.md#tu.NameCollisionError) – If the new name already exists.
  * [**InvalidNameError**](tu.html.md#tu.InvalidNameError) – If the new name is invalid.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.api.run(name, args=None, , capture_output=False, dry_run=False, verbose=False, timeout_override=None, log_output=False, log_dir=None, track_history=True)

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
  * [**UnknownCommandError**](tu.html.md#tu.UnknownCommandError) – If the command is not found and not a dotted name.
  * [**CommandExecutionError**](tu.html.md#tu.CommandExecutionError) – If execution fails.

### tu.api.unregister_command(name)

Unregister a command.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name to unregister.
* **Raises:**
  [**UnknownCommandError**](tu.html.md#tu.UnknownCommandError) – If the command doesn’t exist.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
