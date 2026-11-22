# tu.execute

Command execution for tu.

### Functions

| [`execute_plan`](#tu.execute.execute_plan)(plan[, capture_output])              | Execute an ExecutionPlan.                |
|----------------------------------------------------------------------------------------------------|------------------------------------------|
| [`execute_python_callable`](#tu.execute.execute_python_callable)(target, args[, cwd, ...]) | Execute a Python callable.               |
| [`execute_python_module`](#tu.execute.execute_python_module)(module, args[, cwd, ...])   | Execute a Python module using python -m. |
| [`execute_shell`](#tu.execute.execute_shell)(target, args[, cwd, env, ...])      | Execute a shell command.                 |

### tu.execute.execute_plan(plan, capture_output=False)

Execute an ExecutionPlan.

* **Parameters:**
  * **plan** ([`ExecutionPlan`](tu.models.html.md#tu.models.ExecutionPlan)) – ExecutionPlan to execute.
  * **capture_output** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to capture stdout/stderr.
* **Return type:**
  [`RunResult`](tu.models.html.md#tu.models.RunResult)
* **Returns:**
  RunResult with execution results.

### tu.execute.execute_python_callable(target, args, cwd=None, env=None, capture_output=False, timeout=None, dry_run=False, verbose=False)

Execute a Python callable.

* **Parameters:**
  * **target** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Module:function string (e.g., “mymodule:main”).
  * **args** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Arguments to pass to the callable.
  * **cwd** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Working directory (changes sys.path and os.cwd if provided).
  * **env** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Environment variables (updates os.environ if provided).
  * **capture_output** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to capture stdout/stderr.
  * **timeout** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Timeout in seconds (not supported for callables).
  * **dry_run** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show what would execute without running.
  * **verbose** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show detailed execution information.
* **Return type:**
  [`RunResult`](tu.models.html.md#tu.models.RunResult)
* **Returns:**
  RunResult with execution results.
* **Raises:**
  [**CommandExecutionError**](tu.html.md#tu.CommandExecutionError) – If execution fails.

### tu.execute.execute_python_module(module, args, cwd=None, env=None, capture_output=False, timeout=None, dry_run=False, verbose=False)

Execute a Python module using python -m.

* **Parameters:**
  * **module** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python module to execute.
  * **args** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Arguments to pass to the module.
  * **cwd** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Working directory for execution.
  * **env** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Environment variables.
  * **capture_output** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to capture stdout/stderr.
  * **timeout** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Timeout in seconds.
  * **dry_run** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show what would execute without running.
  * **verbose** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show detailed execution information.
* **Return type:**
  [`RunResult`](tu.models.html.md#tu.models.RunResult)
* **Returns:**
  RunResult with execution results.
* **Raises:**
  [**CommandExecutionError**](tu.html.md#tu.CommandExecutionError) – If execution fails.

### tu.execute.execute_shell(target, args, cwd=None, env=None, capture_output=False, timeout=None, dry_run=False, verbose=False)

Execute a shell command.

* **Parameters:**
  * **target** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Shell command or path to execute.
  * **args** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Arguments to pass to the command.
  * **cwd** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Working directory for execution.
  * **env** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Environment variables.
  * **capture_output** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to capture stdout/stderr.
  * **timeout** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Timeout in seconds.
  * **dry_run** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show what would execute without running.
  * **verbose** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show detailed execution information.
* **Return type:**
  [`RunResult`](tu.models.html.md#tu.models.RunResult)
* **Returns:**
  RunResult with execution results.
* **Raises:**
  [**CommandExecutionError**](tu.html.md#tu.CommandExecutionError) – If execution fails.
