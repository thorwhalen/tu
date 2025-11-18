"""Utility functions for tu."""

import json
import shutil
from pathlib import Path
from typing import Optional

from .models import RegisteredCommand
from .registry import get_registry_path, load_registry, save_registry


def export_registry(output_path: Path, registry_path: Optional[Path] = None) -> None:
    """Export the registry to a file.

    Args:
        output_path: Path to export the registry to.
        registry_path: Optional path to source registry file.
    """
    if registry_path is None:
        registry_path = get_registry_path()

    # Simply copy the registry file
    shutil.copy(registry_path, output_path)


def import_registry(
    input_path: Path,
    merge: bool = False,
    registry_path: Optional[Path] = None
) -> None:
    """Import a registry from a file.

    Args:
        input_path: Path to import the registry from.
        merge: If True, merge with existing registry. If False, replace.
        registry_path: Optional path to target registry file.

    Raises:
        ValueError: If merge=True and there are naming conflicts.
    """
    if registry_path is None:
        registry_path = get_registry_path()

    # Load the import data
    with open(input_path, "r") as f:
        import_data = json.load(f)

    if not merge:
        # Simple replacement
        shutil.copy(input_path, registry_path)
        return

    # Merge mode - load both registries
    existing_commands = load_registry(registry_path)
    import_commands = {}

    for name, cmd_data in import_data.get("commands", {}).items():
        import_commands[name] = RegisteredCommand.from_dict(name, cmd_data)

    # Check for conflicts
    conflicts = set(existing_commands.keys()) & set(import_commands.keys())
    if conflicts:
        raise ValueError(
            f"Cannot merge: the following commands already exist: {', '.join(conflicts)}\n"
            "Either rename or remove these commands first, or import without --merge to replace."
        )

    # Merge and save
    existing_commands.update(import_commands)
    save_registry(existing_commands, registry_path)


def validate_command(command: RegisteredCommand) -> tuple[bool, Optional[str]]:
    """Validate that a command's target exists and is executable.

    Args:
        command: RegisteredCommand to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if command.type == "shell":
        # For shell commands, check if the command exists in PATH
        # or if it's a path, check if the file exists
        target_parts = command.target.split()
        if not target_parts:
            return False, "Empty target"

        cmd = target_parts[0]

        # If it looks like a path, check if file exists
        if "/" in cmd or "\\" in cmd:
            path = Path(cmd)
            if not path.exists():
                return False, f"File not found: {cmd}"
            if not path.is_file():
                return False, f"Not a file: {cmd}"
            # On Unix, check if executable
            import os
            if os.name != "nt" and not os.access(cmd, os.X_OK):
                return False, f"File not executable: {cmd}"
            return True, None
        else:
            # Check if command is in PATH
            if shutil.which(cmd) is None:
                return False, f"Command not found in PATH: {cmd}"
            return True, None

    elif command.type == "python_module":
        # Try to import the module
        import importlib
        try:
            importlib.import_module(command.target)
            return True, None
        except ImportError as e:
            return False, f"Cannot import module: {e}"

    elif command.type == "python_callable":
        # Parse and validate callable
        if ":" not in command.target:
            return False, "Invalid callable format (expected module:function)"

        module_path, function_name = command.target.rsplit(":", 1)

        import importlib
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            return False, f"Cannot import module '{module_path}': {e}"

        if not hasattr(module, function_name):
            return False, f"Module '{module_path}' has no attribute '{function_name}'"

        func = getattr(module, function_name)
        if not callable(func):
            return False, f"'{command.target}' is not callable"

        return True, None

    return True, None


def validate_all_commands(registry_path: Optional[Path] = None) -> dict[str, Optional[str]]:
    """Validate all commands in the registry.

    Args:
        registry_path: Optional path to registry file.

    Returns:
        Dictionary mapping command names to error messages (None if valid).
    """
    commands = load_registry(registry_path)
    results = {}

    for name, command in commands.items():
        is_valid, error = validate_command(command)
        results[name] = error if not is_valid else None

    return results


def get_registry_stats(registry_path: Optional[Path] = None) -> dict:
    """Get statistics about the registry.

    Args:
        registry_path: Optional path to registry file.

    Returns:
        Dictionary with registry statistics.
    """
    commands = load_registry(registry_path)

    # Count by type
    type_counts = {}
    for cmd in commands.values():
        type_counts[cmd.type] = type_counts.get(cmd.type, 0) + 1

    # Count by namespace
    namespace_counts = {}
    for cmd in commands.values():
        if ":" in cmd.name:
            namespace = cmd.name.split(":")[0]
        else:
            namespace = "(root)"
        namespace_counts[namespace] = namespace_counts.get(namespace, 0) + 1

    # Collect all tags
    all_tags = set()
    for cmd in commands.values():
        all_tags.update(cmd.tags)

    return {
        "total_commands": len(commands),
        "by_type": type_counts,
        "by_namespace": namespace_counts,
        "unique_tags": len(all_tags),
        "tags": sorted(all_tags),
    }
