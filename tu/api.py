"""Python API for tu package."""

from datetime import datetime
from typing import Optional

from .exceptions import InvalidNameError, UnknownCommandError
from .execute import execute_plan
from .models import CommandType, ExecutionPlan, RegisteredCommand, RunResult
from .registry import (
    add_command as _add_command,
    get_command,
    list_commands as _list_commands,
    remove_command,
    rename_command as _rename_command,
)
from .resolve import (
    infer_command_type,
    infer_default_name,
    is_dotted_name,
    resolve_command,
    suggest_commands,
    validate_name,
)


def list_commands(pattern: Optional[str] = None) -> list[RegisteredCommand]:
    """List all registered commands.

    Args:
        pattern: Optional pattern to filter command names (substring match).

    Returns:
        List of RegisteredCommand objects.
    """
    return _list_commands(pattern=pattern)


def get_command_info(name: str) -> Optional[RegisteredCommand]:
    """Get information about a registered command.

    Args:
        name: Command name.

    Returns:
        RegisteredCommand if found, None otherwise.
    """
    return get_command(name)


def register_command(
    target: str,
    *,
    name: Optional[str] = None,
    type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    allow_dot_name: bool = False
) -> RegisteredCommand:
    """Register a new command.

    Args:
        target: Target to execute (command, module, callable).
        name: Command name (FQN). If None, inferred from target.
        type: Command type (shell, python_module, python_callable). If None, inferred.
        description: Optional description.
        tags: Optional list of tags.
        allow_dot_name: Allow registering names with dots without confirmation.

    Returns:
        The registered RegisteredCommand.

    Raises:
        NameCollisionError: If the name already exists.
        InvalidNameError: If the name is invalid.
    """
    # Infer type if not provided
    if type is None:
        inferred_type = infer_command_type(target)
    else:
        if type not in ["shell", "python_module", "python_callable"]:
            raise ValueError(f"Invalid command type: {type}")
        inferred_type = type

    # Infer name if not provided
    if name is None:
        inferred_name = infer_default_name(target, inferred_type)
    else:
        inferred_name = name

    # Validate name
    validate_name(inferred_name)

    # Check for dotted name
    if is_dotted_name(inferred_name) and not allow_dot_name:
        raise InvalidNameError(
            f"Name '{inferred_name}' contains a dot, which conflicts with the "
            "dotted-name rule for Python modules. If you want to register this name anyway, "
            "use allow_dot_name=True."
        )

    # Create command
    command = RegisteredCommand(
        name=inferred_name,
        type=inferred_type,
        target=target,
        description=description,
        tags=tags or [],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Add to registry
    _add_command(command)

    return command


def unregister_command(name: str) -> None:
    """Unregister a command.

    Args:
        name: Command name to unregister.

    Raises:
        UnknownCommandError: If the command doesn't exist.
    """
    remove_command(name)


def rename_command(old_name: str, new_name: str) -> None:
    """Rename a command.

    Args:
        old_name: Current name of the command.
        new_name: New name for the command.

    Raises:
        UnknownCommandError: If the old command doesn't exist.
        NameCollisionError: If the new name already exists.
        InvalidNameError: If the new name is invalid.
    """
    # Validate new name
    validate_name(new_name)

    # Rename in registry
    _rename_command(old_name, new_name)


def run(
    name: str,
    args: Optional[list[str]] = None,
    *,
    capture_output: bool = False
) -> RunResult:
    """Run a command.

    Args:
        name: Command name to run.
        args: Arguments to pass to the command.
        capture_output: Whether to capture stdout/stderr.

    Returns:
        RunResult with execution results.

    Raises:
        UnknownCommandError: If the command is not found and not a dotted name.
        CommandExecutionError: If execution fails.
    """
    if args is None:
        args = []

    # Resolve command
    command, is_dotted = resolve_command(name)

    if command is not None:
        # Execute registered command
        plan = ExecutionPlan(
            command_type=command.type,
            target=command.target,
            args=args
        )
        return execute_plan(plan, capture_output=capture_output)

    elif is_dotted:
        # Execute dotted name as Python module
        plan = ExecutionPlan(
            command_type="python_module",
            target=name,
            args=args
        )
        return execute_plan(plan, capture_output=capture_output)

    else:
        # Not found - suggest alternatives
        suggestions = suggest_commands(name)
        if suggestions:
            raise UnknownCommandError(
                f"Unknown command: {name}\n"
                f"Did you mean one of these?\n" +
                "\n".join(f"  - {s}" for s in suggestions)
            )
        else:
            raise UnknownCommandError(f"Unknown command: {name}")
