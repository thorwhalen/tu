# tu.exceptions

Custom exceptions for the tu package.

### Exceptions

| [`CommandExecutionError`](#tu.exceptions.CommandExecutionError)   | Raised when a command fails to execute.                             |
|--------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`InvalidCommandTypeError`](#tu.exceptions.InvalidCommandTypeError) | Raised when an invalid command type is specified.                   |
| [`InvalidNameError`](#tu.exceptions.InvalidNameError)        | Raised when a command name is invalid.                              |
| [`NameCollisionError`](#tu.exceptions.NameCollisionError)      | Raised when attempting to register a command with an existing name. |
| [`RegistryCorruptedError`](#tu.exceptions.RegistryCorruptedError)  | Raised when the registry file is corrupted or invalid.              |
| [`TuError`](#tu.exceptions.TuError)                 | Base exception for all tu errors.                                   |
| [`UnknownCommandError`](#tu.exceptions.UnknownCommandError)     | Raised when a command is not found in the registry.                 |

### *exception* tu.exceptions.CommandExecutionError

Bases: [`TuError`](#tu.exceptions.TuError)

Raised when a command fails to execute.

### *exception* tu.exceptions.InvalidCommandTypeError

Bases: [`TuError`](#tu.exceptions.TuError)

Raised when an invalid command type is specified.

### *exception* tu.exceptions.InvalidNameError

Bases: [`TuError`](#tu.exceptions.TuError)

Raised when a command name is invalid.

### *exception* tu.exceptions.NameCollisionError

Bases: [`TuError`](#tu.exceptions.TuError)

Raised when attempting to register a command with an existing name.

### *exception* tu.exceptions.RegistryCorruptedError

Bases: [`TuError`](#tu.exceptions.TuError)

Raised when the registry file is corrupted or invalid.

### *exception* tu.exceptions.TuError

Bases: [`Exception`](https://docs.python.org/3/builtins/exceptions.html#Exception)

Base exception for all tu errors.

### *exception* tu.exceptions.UnknownCommandError

Bases: [`TuError`](#tu.exceptions.TuError)

Raised when a command is not found in the registry.
