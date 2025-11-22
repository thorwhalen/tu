"""Python API for tu package."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .exceptions import InvalidNameError, UnknownCommandError
from .execute import execute_plan
from .history import add_history_entry
from .log import write_log
from .models import CommandType, ExecutionPlan, HistoryEntry, RegisteredCommand, RunResult
from .registry import (
    add_command as _add_command,
    get_command,
    list_commands as _list_commands,
    load_layered_registry,
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


def list_commands(pattern: Optional[str] = None, use_layered: bool = True) -> list[RegisteredCommand]:
    """List all registered commands.

    Args:
        pattern: Optional pattern to filter command names (substring match).
        use_layered: If True, include project-local commands.

    Returns:
        List of RegisteredCommand objects.
    """
    if use_layered:
        # Load layered registry (project + global)
        commands_dict = load_layered_registry()
        commands = list(commands_dict.values())

        if pattern is None:
            return sorted(commands, key=lambda c: c.name)

        # Filter by pattern
        pattern_lower = pattern.lower()
        return sorted(
            [c for c in commands if pattern_lower in c.name.lower()],
            key=lambda c: c.name
        )
    else:
        return _list_commands(pattern=pattern)


def get_command_info(name: str, use_layered: bool = True) -> Optional[RegisteredCommand]:
    """Get information about a registered command.

    Args:
        name: Command name or alias.
        use_layered: If True, search project-local registry too.

    Returns:
        RegisteredCommand if found, None otherwise.
    """
    if use_layered:
        # Try to resolve using layered registry
        command, _ = resolve_command(name)
        return command
    else:
        return get_command(name)


def register_command(
    target: str,
    *,
    name: Optional[str] = None,
    type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    aliases: Optional[list[str]] = None,
    depends_on: Optional[list[str]] = None,
    env: Optional[dict[str, str]] = None,
    timeout: Optional[int] = None,
    allow_dot_name: bool = False
) -> RegisteredCommand:
    """Register a new command.

    Args:
        target: Target to execute (command, module, callable).
        name: Command name (FQN). If None, inferred from target.
        type: Command type (shell, python_module, python_callable). If None, inferred.
        description: Optional description.
        tags: Optional list of tags.
        aliases: Optional list of alternative names.
        depends_on: Optional list of commands this depends on.
        env: Optional environment variables to set.
        timeout: Optional timeout in seconds.
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
        aliases=aliases or [],
        depends_on=depends_on or [],
        env=env or {},
        timeout=timeout,
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
    capture_output: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
    timeout_override: Optional[int] = None,
    log_output: bool = False,
    log_dir: Optional[Path] = None,
    track_history: bool = True
) -> RunResult:
    """Run a command.

    Args:
        name: Command name to run.
        args: Arguments to pass to the command.
        capture_output: Whether to capture stdout/stderr.
        dry_run: If True, show what would execute without running.
        verbose: If True, show detailed execution information.
        timeout_override: Override the command's timeout setting.
        log_output: If True, write output to log file.
        log_dir: Optional directory for log files.
        track_history: If True, add to command history.

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
        # Handle dependencies
        if command.depends_on and not dry_run:
            if verbose:
                print(f"[VERBOSE] Running dependencies: {', '.join(command.depends_on)}")
            for dep in command.depends_on:
                dep_result = run(dep, verbose=verbose, track_history=False)
                if dep_result.returncode != 0:
                    raise UnknownCommandError(
                        f"Dependency '{dep}' failed with exit code {dep_result.returncode}"
                    )

        # Build execution plan
        timeout = timeout_override if timeout_override is not None else command.timeout

        # Merge command env with current env
        merged_env = dict(os.environ)
        if command.env:
            merged_env.update(command.env)

        plan = ExecutionPlan(
            command_type=command.type,
            target=command.target,
            args=args,
            env=merged_env if command.env else None,
            timeout=timeout,
            dry_run=dry_run,
            verbose=verbose
        )

        result = execute_plan(plan, capture_output=capture_output or log_output)

        # Log output if requested
        if log_output and not dry_run:
            log_file = write_log(command.name, result, args, log_dir)
            if verbose:
                print(f"[VERBOSE] Output logged to: {log_file}")

        # Track history if requested
        if track_history and not dry_run:
            entry = HistoryEntry(
                command_name=command.name,
                args=args,
                returncode=result.returncode,
                executed_at=datetime.now(),
                duration=result.duration or 0.0,
                cwd=os.getcwd()
            )
            add_history_entry(entry)

        return result

    elif is_dotted:
        # Execute dotted name as Python module
        plan = ExecutionPlan(
            command_type="python_module",
            target=name,
            args=args,
            dry_run=dry_run,
            verbose=verbose
        )

        result = execute_plan(plan, capture_output=capture_output or log_output)

        # Log output if requested
        if log_output and not dry_run:
            log_file = write_log(name, result, args, log_dir)
            if verbose:
                print(f"[VERBOSE] Output logged to: {log_file}")

        # Track history if requested
        if track_history and not dry_run:
            entry = HistoryEntry(
                command_name=name,
                args=args,
                returncode=result.returncode,
                executed_at=datetime.now(),
                duration=result.duration or 0.0,
                cwd=os.getcwd()
            )
            add_history_entry(entry)

        return result

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
