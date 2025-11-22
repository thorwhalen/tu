"""Registry management for tu commands."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .exceptions import (
    NameCollisionError,
    RegistryCorruptedError,
    UnknownCommandError,
)
from .models import CommandType, RegisteredCommand


def get_registry_path() -> Path:
    """Get the path to the global registry file.

    Returns:
        Path to the registry JSON file, either from environment variable
        IC_REGISTERED_SCRIPTS_JSON_FILE or default location.
    """
    env_path = os.environ.get("IC_REGISTERED_SCRIPTS_JSON_FILE")
    if env_path:
        return Path(env_path)

    # Default: ~/.config/tu/registered_scripts.json
    config_dir = Path.home() / ".config" / "tu"
    return config_dir / "registered_scripts.json"


def get_project_registry_path() -> Optional[Path]:
    """Get the path to a project-local registry if it exists.

    Searches up the directory tree from the current working directory
    for a .tu/registry.json file.

    Returns:
        Path to project registry if found, None otherwise.
    """
    current = Path.cwd()

    # Search up to root
    while current != current.parent:
        project_registry = current / ".tu" / "registry.json"
        if project_registry.exists():
            return project_registry
        current = current.parent

    return None


def load_registry(path: Optional[Path] = None) -> dict[str, RegisteredCommand]:
    """Load the registry from disk.

    Args:
        path: Optional path to registry file. If None, uses default path.

    Returns:
        Dictionary mapping command names to RegisteredCommand objects.

    Raises:
        RegistryCorruptedError: If the registry file is invalid.
    """
    if path is None:
        path = get_registry_path()

    if not path.exists():
        return {}

    try:
        with open(path, "r") as f:
            data = json.load(f)

        # Handle schema version
        version = data.get("version", 1)
        if version != 1:
            raise RegistryCorruptedError(
                f"Unsupported registry version: {version}. "
                "Please back up and recreate your registry."
            )

        # Load commands
        commands = {}
        for name, cmd_data in data.get("commands", {}).items():
            commands[name] = RegisteredCommand.from_dict(name, cmd_data)

        return commands

    except json.JSONDecodeError as e:
        raise RegistryCorruptedError(
            f"Registry file is corrupted: {e}. "
            "Please back up and recreate your registry."
        )
    except Exception as e:
        raise RegistryCorruptedError(
            f"Failed to load registry: {e}. "
            "Please check your registry file."
        )


def load_layered_registry() -> dict[str, RegisteredCommand]:
    """Load registry with project-local commands layered over global commands.

    Project-local commands (from .tu/registry.json) take precedence over
    global commands when there are naming conflicts.

    Returns:
        Dictionary mapping command names to RegisteredCommand objects.
    """
    # Load global registry
    global_commands = load_registry()

    # Load project-local registry if it exists
    project_path = get_project_registry_path()
    if project_path is None:
        return global_commands

    project_commands = load_registry(project_path)

    # Merge: project commands override global
    result = global_commands.copy()
    result.update(project_commands)

    return result


def save_registry(
    commands: dict[str, RegisteredCommand],
    path: Optional[Path] = None
) -> None:
    """Save the registry to disk.

    Args:
        commands: Dictionary mapping command names to RegisteredCommand objects.
        path: Optional path to registry file. If None, uses default path.
    """
    if path is None:
        path = get_registry_path()

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Build registry structure
    data = {
        "version": 1,
        "commands": {
            name: cmd.to_dict()
            for name, cmd in commands.items()
        }
    }

    # Atomic write: write to temp file, then rename
    temp_path = path.with_suffix(".tmp")
    try:
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2)
        temp_path.replace(path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise


def add_command(
    command: RegisteredCommand,
    path: Optional[Path] = None
) -> None:
    """Add a command to the registry.

    Args:
        command: RegisteredCommand to add.
        path: Optional path to registry file.

    Raises:
        NameCollisionError: If a command with the same name already exists.
    """
    commands = load_registry(path)

    if command.name in commands:
        raise NameCollisionError(
            f"Command '{command.name}' already exists. "
            f"Use 'tu --unregister {command.name}' to remove it, "
            f"or 'tu --rename {command.name} <new_name>' to rename it."
        )

    commands[command.name] = command
    save_registry(commands, path)


def remove_command(name: str, path: Optional[Path] = None) -> None:
    """Remove a command from the registry.

    Args:
        name: Name of the command to remove.
        path: Optional path to registry file.

    Raises:
        UnknownCommandError: If the command doesn't exist.
    """
    commands = load_registry(path)

    if name not in commands:
        raise UnknownCommandError(
            f"Command '{name}' not found in registry."
        )

    del commands[name]
    save_registry(commands, path)


def rename_command(
    old_name: str,
    new_name: str,
    path: Optional[Path] = None
) -> None:
    """Rename a command in the registry.

    Args:
        old_name: Current name of the command.
        new_name: New name for the command.
        path: Optional path to registry file.

    Raises:
        UnknownCommandError: If the old command doesn't exist.
        NameCollisionError: If the new name already exists.
    """
    commands = load_registry(path)

    if old_name not in commands:
        raise UnknownCommandError(
            f"Command '{old_name}' not found in registry."
        )

    if new_name in commands:
        raise NameCollisionError(
            f"Command '{new_name}' already exists. "
            f"Use 'tu --unregister {new_name}' to remove it first."
        )

    # Update the command
    command = commands[old_name]
    command.name = new_name
    command.updated_at = datetime.now()

    # Remove old, add new
    del commands[old_name]
    commands[new_name] = command

    save_registry(commands, path)


def get_command(name: str, path: Optional[Path] = None) -> Optional[RegisteredCommand]:
    """Get a command from the registry.

    Args:
        name: Name of the command.
        path: Optional path to registry file.

    Returns:
        RegisteredCommand if found, None otherwise.
    """
    commands = load_registry(path)
    return commands.get(name)


def list_commands(
    pattern: Optional[str] = None,
    path: Optional[Path] = None
) -> list[RegisteredCommand]:
    """List all commands in the registry.

    Args:
        pattern: Optional pattern to filter command names (substring match).
        path: Optional path to registry file.

    Returns:
        List of RegisteredCommand objects.
    """
    commands = load_registry(path)

    if pattern is None:
        return sorted(commands.values(), key=lambda c: c.name)

    # Filter by pattern (case-insensitive substring match)
    pattern_lower = pattern.lower()
    return sorted(
        [c for c in commands.values() if pattern_lower in c.name.lower()],
        key=lambda c: c.name
    )
