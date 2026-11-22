# tu.resolve

Command name resolution for tu.

### Functions

| [`infer_command_type`](#tu.resolve.infer_command_type)(target)                | Infer command type from target string.          |
|--------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`infer_default_name`](#tu.resolve.infer_default_name)(target, command_type)  | Infer a default command name from the target.   |
| [`is_dotted_name`](#tu.resolve.is_dotted_name)(name)                      | Check if a name is a dotted Python module name. |
| [`resolve_command`](#tu.resolve.resolve_command)(name)                     | Resolve a command name to a RegisteredCommand.  |
| [`suggest_commands`](#tu.resolve.suggest_commands)(name[, max_suggestions]) | Suggest similar command names.                  |
| [`validate_name`](#tu.resolve.validate_name)(name)                       | Validate a command name.                        |

### tu.resolve.infer_command_type(target)

Infer command type from target string.

* **Parameters:**
  **target** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target string to analyze.
* **Return type:**
  [`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'shell'`, `'python_module'`, `'python_callable'`]
* **Returns:**
  Inferred command type.

### tu.resolve.infer_default_name(target, command_type)

Infer a default command name from the target.

* **Parameters:**
  * **target** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target string.
  * **command_type** ([`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'shell'`, `'python_module'`, `'python_callable'`]) – Type of command.
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Inferred default name.

### tu.resolve.is_dotted_name(name)

Check if a name is a dotted Python module name.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name to check.
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if the name contains a dot (potential Python module).

### tu.resolve.resolve_command(name)

Resolve a command name to a RegisteredCommand.

Supports resolving by command name or alias.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name or alias to resolve.
* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)], [`bool`](https://docs.python.org/3/builtins/functions.html#bool)]
* **Returns:**
  Tuple of (RegisteredCommand or None, is_dotted_fallback).
  If found in registry: (command, False)
  If using dotted-name rule: (None, True)
  If not found: (None, False)

### tu.resolve.suggest_commands(name, max_suggestions=5)

Suggest similar command names.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name that wasn’t found.
  * **max_suggestions** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Maximum number of suggestions to return.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of suggested command names.

### tu.resolve.validate_name(name)

Validate a command name.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Command name to validate.
* **Raises:**
  [**InvalidNameError**](tu.html.md#tu.InvalidNameError) – If the name is invalid.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
