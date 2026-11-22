# tu.models

Data models for the tu package.

### Classes

| [`ExecutionPlan`](#tu.models.ExecutionPlan)(command_type, target[, args, ...])   | Plan for executing a command.                       |
|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| [`HistoryEntry`](#tu.models.HistoryEntry)(command_name, args, returncode, ...)  | Entry in command execution history.                 |
| [`RegisteredCommand`](#tu.models.RegisteredCommand)(name, type, target[, ...])       | Represents a registered command in the tu registry. |
| [`RunResult`](#tu.models.RunResult)(returncode[, stdout, stderr, duration])  | Result of running a command.                        |

### *class* tu.models.ExecutionPlan(command_type, target, args=list(), cwd=None, env=None, timeout=None, dry_run=False, verbose=False)

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

### *class* tu.models.HistoryEntry(command_name, args, returncode, executed_at, duration, cwd=None)

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
  [`HistoryEntry`](#tu.models.HistoryEntry)

#### to_dict()

Convert to dictionary for JSON serialization.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* tu.models.RegisteredCommand(name, type, target, description=None, tags=list(), created_at=datetime.now(), updated_at=datetime.now(), aliases=list(), depends_on=list(), env=dict(), timeout=None)

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
  [`RegisteredCommand`](#tu.models.RegisteredCommand)

#### to_dict()

Convert to dictionary for JSON serialization.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* tu.models.RunResult(returncode, stdout=None, stderr=None, duration=None)

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
