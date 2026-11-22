# tu.completion

Shell completion support for tu.

### Functions

| [`check_completion_hint`](#tu.completion.check_completion_hint)()            | Return a hint string if completion is not installed, else None.          |
|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| [`get_completion_candidates`](#tu.completion.get_completion_candidates)(partial) | Get command name candidates for completion.                              |
| [`get_completion_script`](#tu.completion.get_completion_script)(shell)       | Get completion script for a specific shell.                              |
| [`get_flag_candidates`](#tu.completion.get_flag_candidates)(partial)       | Get flag candidates for completion.                                      |
| [`install_completion`](#tu.completion.install_completion)(shell[, yes])   | Install the completion script for the given shell.                       |
| [`is_completion_installed`](#tu.completion.is_completion_installed)([shell])   | Check whether the tu completion script is installed for the given shell. |

### tu.completion.check_completion_hint()

Return a hint string if completion is not installed, else None.

Uses a stamp file to avoid nagging on every invocation — shows the hint
at most once per day.

* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### tu.completion.get_completion_candidates(partial)

Get command name candidates for completion.

* **Parameters:**
  **partial** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Partial command name typed by user.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of matching command names.

### tu.completion.get_completion_script(shell)

Get completion script for a specific shell.

* **Parameters:**
  **shell** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Shell name (bash, zsh, fish).
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Completion script content.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If shell is not supported.

### tu.completion.get_flag_candidates(partial)

Get flag candidates for completion.

* **Parameters:**
  **partial** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Partial flag typed by user (e.g. ‘–n’ or ‘–‘).
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of matching flags.

### tu.completion.install_completion(shell, yes=False)

Install the completion script for the given shell.

Finds the appropriate directory, asks for confirmation, writes the file.

* **Parameters:**
  * **shell** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Shell name (bash, zsh, fish).
  * **yes** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Skip confirmation prompt.
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Status message describing what was done.

### tu.completion.is_completion_installed(shell=None)

Check whether the tu completion script is installed for the given shell.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
