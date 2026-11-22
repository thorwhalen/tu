# tu.log

Command output logging for tu.

### Functions

| [`clear_old_logs`](#tu.log.clear_old_logs)([days])                           | Clear log files older than specified days.   |
|---------------------------------------------------------------------------------------------------|----------------------------------------------|
| [`get_log_directory`](#tu.log.get_log_directory)()                              | Get the default log directory.               |
| [`get_recent_logs`](#tu.log.get_recent_logs)([command_name, limit])           | Get recent log files.                        |
| [`write_log`](#tu.log.write_log)(command_name, result, args[, log_dir]) | Write command output to a log file.          |

### tu.log.clear_old_logs(days=30)

Clear log files older than specified days.

* **Parameters:**
  **days** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Number of days to keep logs for.
* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)
* **Returns:**
  Number of log files deleted.

### tu.log.get_log_directory()

Get the default log directory.

* **Return type:**
  [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)
* **Returns:**
  Path to the log directory.

### tu.log.get_recent_logs(command_name=None, limit=10)

Get recent log files.

* **Parameters:**
  * **command_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional command name to filter by.
  * **limit** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Maximum number of log files to return.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]
* **Returns:**
  List of log file paths, ordered by modification time (most recent first).

### tu.log.write_log(command_name, result, args, log_dir=None)

Write command output to a log file.

* **Parameters:**
  * **command_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the command that was executed.
  * **result** ([`RunResult`](tu.models.html.md#tu.models.RunResult)) – RunResult from execution.
  * **args** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Arguments passed to the command.
  * **log_dir** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]) – Optional log directory. If None, uses default.
* **Return type:**
  [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)
* **Returns:**
  Path to the log file that was written.
