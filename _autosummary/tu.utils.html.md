# tu.utils

Utility functions for tu.

### Functions

| [`export_registry`](#tu.utils.export_registry)(output_path[, registry_path])   | Export the registry to a file.                             |
|--------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`get_registry_stats`](#tu.utils.get_registry_stats)([registry_path])             | Get statistics about the registry.                         |
| [`import_registry`](#tu.utils.import_registry)(input_path[, merge, ...])       | Import a registry from a file.                             |
| [`validate_all_commands`](#tu.utils.validate_all_commands)([registry_path])          | Validate all commands in the registry.                     |
| [`validate_command`](#tu.utils.validate_command)(command)                       | Validate that a command's target exists and is executable. |

### tu.utils.export_registry(output_path, registry_path=None)

Export the registry to a file.

* **Parameters:**
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to export the registry to.
  * **registry_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to source registry file.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.utils.get_registry_stats(registry_path=None)

Get statistics about the registry.

* **Parameters:**
  **registry_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dictionary with registry statistics.

### tu.utils.import_registry(input_path, merge=False, registry_path=None)

Import a registry from a file.

* **Parameters:**
  * **input_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to import the registry from.
  * **merge** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, merge with existing registry. If False, replace.
  * **registry_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to target registry file.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If merge=True and there are naming conflicts.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.utils.validate_all_commands(registry_path=None)

Validate all commands in the registry.

* **Parameters:**
  **registry_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  Dictionary mapping command names to error messages (None if valid).

### tu.utils.validate_command(command)

Validate that a command’s target exists and is executable.

* **Parameters:**
  **command** ([`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)) – RegisteredCommand to validate.
* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`bool`](https://docs.python.org/3/builtins/functions.html#bool), [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  Tuple of (is_valid, error_message).
