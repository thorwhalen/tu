# tu.history

Command execution history tracking.

### Functions

| [`add_history_entry`](#tu.history.add_history_entry)(entry[, max_entries])    | Add an entry to command history.    |
|---------------------------------------------------------------------------------------------|-------------------------------------|
| [`clear_history`](#tu.history.clear_history)()                            | Clear all command history.          |
| [`get_command_history`](#tu.history.get_command_history)(command_name[, limit]) | Get history for a specific command. |
| [`get_history_path`](#tu.history.get_history_path)()                         | Get the path to the history file.   |
| [`load_history`](#tu.history.load_history)([path, limit])                | Load command execution history.     |
| [`save_history`](#tu.history.save_history)(entries[, path])              | Save command execution history.     |

### tu.history.add_history_entry(entry, max_entries=1000)

Add an entry to command history.

* **Parameters:**
  * **entry** ([`HistoryEntry`](tu.models.html.md#tu.models.HistoryEntry)) – HistoryEntry to add.
  * **max_entries** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Maximum number of entries to keep (oldest removed first).
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.history.clear_history()

Clear all command history.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### tu.history.get_command_history(command_name, limit=None)

Get history for a specific command.

* **Parameters:**
  * **command_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the command to get history for.
  * **limit** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Optional limit on number of entries.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`HistoryEntry`](tu.models.html.md#tu.models.HistoryEntry)]
* **Returns:**
  List of HistoryEntry objects for the specified command.

### tu.history.get_history_path()

Get the path to the history file.

* **Return type:**
  [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)
* **Returns:**
  Path to the history JSON file.

### tu.history.load_history(path=None, limit=None)

Load command execution history.

* **Parameters:**
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to history file.
  * **limit** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Optional limit on number of entries to load (most recent first).
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`HistoryEntry`](tu.models.html.md#tu.models.HistoryEntry)]
* **Returns:**
  List of HistoryEntry objects, ordered from most recent to oldest.

### tu.history.save_history(entries, path=None)

Save command execution history.

* **Parameters:**
  * **entries** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`HistoryEntry`](tu.models.html.md#tu.models.HistoryEntry)]) – List of HistoryEntry objects.
  * **path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional path to history file.
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
