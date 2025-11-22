"""Command name resolution for tu."""

import difflib
from typing import Optional

from .exceptions import InvalidNameError, UnknownCommandError
from .models import CommandType, RegisteredCommand
from .registry import get_command, list_commands


def is_dotted_name(name: str) -> bool:
    """Check if a name is a dotted Python module name.

    Args:
        name: Command name to check.

    Returns:
        True if the name contains a dot (potential Python module).
    """
    return "." in name


def validate_name(name: str) -> None:
    """Validate a command name.

    Args:
        name: Command name to validate.

    Raises:
        InvalidNameError: If the name is invalid.
    """
    if not name:
        raise InvalidNameError("Command name cannot be empty.")

    # Check for invalid characters
    # Allow: alphanumeric, underscore, dash, dot, colon
    # Colon is used for namespace separators
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.:")
    if not all(c in valid_chars for c in name):
        raise InvalidNameError(
            f"Invalid command name '{name}'. "
            "Only alphanumeric characters, underscores, dashes, dots, and colons are allowed."
        )

    # Check for consecutive colons
    if "::" in name:
        raise InvalidNameError(
            f"Invalid command name '{name}'. "
            "Double colons are not allowed."
        )

    # Check for leading/trailing colons
    if name.startswith(":") or name.endswith(":"):
        raise InvalidNameError(
            f"Invalid command name '{name}'. "
            "Command names cannot start or end with a colon."
        )


def infer_command_type(target: str) -> CommandType:
    """Infer command type from target string.

    Args:
        target: Target string to analyze.

    Returns:
        Inferred command type.
    """
    # Check for python_callable pattern: module:function
    # Format is module:function or package.module:function
    if ":" in target and " " not in target:
        # Looks like module:function
        parts = target.split(":")
        if len(parts) == 2:
            # If it has a colon and no spaces, treat as callable
            return "python_callable"

    # Check for python_module pattern: dotted name
    if "." in target and " " not in target:
        # Try to import to confirm it's a module
        try:
            # Don't actually import, just check the pattern
            # A simple heuristic: if it looks like a.b.c and no slashes, it's probably a module
            if "/" not in target and "\\" not in target:
                return "python_module"
        except:
            pass

    # Default to shell command
    return "shell"


def infer_default_name(target: str, command_type: CommandType) -> str:
    """Infer a default command name from the target.

    Args:
        target: Target string.
        command_type: Type of command.

    Returns:
        Inferred default name.
    """
    if command_type == "python_module":
        # Use last segment: mypkg.mymodule -> mymodule
        return target.split(".")[-1]

    elif command_type == "python_callable":
        # Use function name: mypkg.mymodule:main -> main
        if ":" in target:
            return target.split(":")[-1]
        return target.split(".")[-1]

    else:  # shell
        # If it's a path, use basename
        if "/" in target or "\\" in target:
            import os
            return os.path.basename(target)
        # If it's a simple command, use as-is
        return target.split()[0] if " " in target else target


def resolve_command(name: str) -> tuple[Optional[RegisteredCommand], bool]:
    """Resolve a command name to a RegisteredCommand.

    Supports resolving by command name or alias.

    Args:
        name: Command name or alias to resolve.

    Returns:
        Tuple of (RegisteredCommand or None, is_dotted_fallback).
        If found in registry: (command, False)
        If using dotted-name rule: (None, True)
        If not found: (None, False)
    """
    # First, try to find in registry by name
    command = get_command(name)
    if command is not None:
        return (command, False)

    # Try to find by alias
    all_commands = list_commands()
    for cmd in all_commands:
        if name in cmd.aliases:
            return (cmd, False)

    # If not found and contains a dot, use dotted-name rule
    if is_dotted_name(name):
        return (None, True)

    # Not found
    return (None, False)


def suggest_commands(name: str, max_suggestions: int = 5) -> list[str]:
    """Suggest similar command names.

    Args:
        name: Command name that wasn't found.
        max_suggestions: Maximum number of suggestions to return.

    Returns:
        List of suggested command names.
    """
    all_commands = list_commands()
    all_names = [cmd.name for cmd in all_commands]

    # Use difflib to find close matches
    suggestions = difflib.get_close_matches(
        name,
        all_names,
        n=max_suggestions,
        cutoff=0.6
    )

    return suggestions
