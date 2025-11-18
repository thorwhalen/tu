"""tu - Terminal Utils: Quick access to your favorite scripts.

A unified entry point for running scripts and commands with a hierarchical namespace.
"""

from .api import (
    get_command_info,
    list_commands,
    register_command,
    rename_command,
    run,
    unregister_command,
)
from .exceptions import (
    CommandExecutionError,
    InvalidCommandTypeError,
    InvalidNameError,
    NameCollisionError,
    RegistryCorruptedError,
    TuError,
    UnknownCommandError,
)
from .models import CommandType, ExecutionPlan, HistoryEntry, RegisteredCommand, RunResult

__version__ = "0.0.1"

__all__ = [
    # API functions
    "list_commands",
    "get_command_info",
    "register_command",
    "unregister_command",
    "rename_command",
    "run",
    # Models
    "RegisteredCommand",
    "RunResult",
    "ExecutionPlan",
    "HistoryEntry",
    "CommandType",
    # Exceptions
    "TuError",
    "UnknownCommandError",
    "NameCollisionError",
    "RegistryCorruptedError",
    "InvalidCommandTypeError",
    "InvalidNameError",
    "CommandExecutionError",
]
