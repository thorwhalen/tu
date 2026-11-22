# tu.registry

Registry management for tu commands.

### Functions

| [`add_command`](#tu.registry.add_command)(command[, path])               | Add a command to the registry.                                          |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| [`get_command`](#tu.registry.get_command)(name[, path])                  | Get a command from the registry.                                        |
| [`get_project_registry_path`](#tu.registry.get_project_registry_path)()                | Get the path to a project-local registry if it exists.                  |
| [`get_registry_path`](#tu.registry.get_registry_path)()                        | Get the path to the global registry file.                               |
| [`list_commands`](#tu.registry.list_commands)([pattern, path])             | List all commands in the registry.                                      |
| [`load_layered_registry`](#tu.registry.load_layered_registry)()                    | Load registry with project-local commands layered over global commands. |
| [`load_registry`](#tu.registry.load_registry)([path])                      | Load the registry from disk.                                            |
| [`remove_command`](#tu.registry.remove_command)(name[, path])               | Remove a command from the registry.                                     |
| [`rename_command`](#tu.registry.rename_command)(old_name, new_name[, path]) | Rename a command in the registry.                                       |
| [`save_registry`](#tu.registry.save_registry)(commands[, path])            | Save the registry to disk.                                              |

### tu.registry.add_command(command, path=None)

Add a command to the registry.

* **Parameters:**
  * **command** ([`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)) – RegisteredCommand to add.
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Raises:**
  [**NameCollisionError**](tu.html.md#tu.NameCollisionError) – If a command with the same name already exists.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.registry.get_command(name, path=None)

Get a command from the registry.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the command.
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  RegisteredCommand if found, None otherwise.

### tu.registry.get_project_registry_path()

Get the path to a project-local registry if it exists.

Searches up the directory tree from the current working directory
for a .tu/registry.json file.

* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]
* **Returns:**
  Path to project registry if found, None otherwise.

### tu.registry.get_registry_path()

Get the path to the global registry file.

* **Return type:**
  [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)
* **Returns:**
  Path to the registry JSON file, either from environment variable
  IC_REGISTERED_SCRIPTS_JSON_FILE or default location.

### tu.registry.list_commands(pattern=None, path=None)

List all commands in the registry.

* **Parameters:**
  * **pattern** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional pattern to filter command names (substring match).
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  List of RegisteredCommand objects.

### tu.registry.load_layered_registry()

Load registry with project-local commands layered over global commands.

Project-local commands (from .tu/registry.json) take precedence over
global commands when there are naming conflicts.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  Dictionary mapping command names to RegisteredCommand objects.

### tu.registry.load_registry(path=None)

Load the registry from disk.

* **Parameters:**
  **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file. If None, uses default path.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]
* **Returns:**
  Dictionary mapping command names to RegisteredCommand objects.
* **Raises:**
  [**RegistryCorruptedError**](tu.html.md#tu.RegistryCorruptedError) – If the registry file is invalid.

### tu.registry.remove_command(name, path=None)

Remove a command from the registry.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the command to remove.
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Raises:**
  [**UnknownCommandError**](tu.html.md#tu.UnknownCommandError) – If the command doesn’t exist.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.registry.rename_command(old_name, new_name, path=None)

Rename a command in the registry.

* **Parameters:**
  * **old_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Current name of the command.
  * **new_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – New name for the command.
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file.
* **Raises:**
  * [**UnknownCommandError**](tu.html.md#tu.UnknownCommandError) – If the old command doesn’t exist.
  * [**NameCollisionError**](tu.html.md#tu.NameCollisionError) – If the new name already exists.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.registry.save_registry(commands, path=None)

Save the registry to disk.

* **Parameters:**
  * **commands** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`RegisteredCommand`](tu.models.html.md#tu.models.RegisteredCommand)]) – Dictionary mapping command names to RegisteredCommand objects.
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to registry file. If None, uses default path.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
