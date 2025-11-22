"""Tests for the registry module."""

from datetime import datetime
from pathlib import Path

import pytest

from tu.exceptions import NameCollisionError, UnknownCommandError
from tu.models import RegisteredCommand
from tu.registry import (
    add_command,
    get_command,
    list_commands,
    load_registry,
    remove_command,
    rename_command,
    save_registry,
)


def test_load_empty_registry(temp_registry: Path):
    """Test loading an empty registry."""
    commands = load_registry(temp_registry)
    assert commands == {}


def test_save_and_load_registry(temp_registry: Path):
    """Test saving and loading a registry."""
    commands = {
        "test": RegisteredCommand(
            name="test",
            type="shell",
            target="echo hello",
            description="Test command",
            tags=["test"],
        )
    }

    save_registry(commands, temp_registry)
    loaded = load_registry(temp_registry)

    assert len(loaded) == 1
    assert "test" in loaded
    assert loaded["test"].name == "test"
    assert loaded["test"].type == "shell"
    assert loaded["test"].target == "echo hello"


def test_add_command(temp_registry: Path):
    """Test adding a command to the registry."""
    cmd = RegisteredCommand(
        name="mycommand",
        type="python_module",
        target="mymodule",
        description="My command",
    )

    add_command(cmd, temp_registry)

    commands = load_registry(temp_registry)
    assert "mycommand" in commands
    assert commands["mycommand"].target == "mymodule"


def test_add_duplicate_command(temp_registry: Path):
    """Test that adding a duplicate command raises an error."""
    cmd = RegisteredCommand(
        name="duplicate",
        type="shell",
        target="echo test",
    )

    add_command(cmd, temp_registry)

    with pytest.raises(NameCollisionError):
        add_command(cmd, temp_registry)


def test_remove_command(temp_registry: Path):
    """Test removing a command from the registry."""
    cmd = RegisteredCommand(
        name="toremove",
        type="shell",
        target="echo test",
    )

    add_command(cmd, temp_registry)
    assert get_command("toremove", temp_registry) is not None

    remove_command("toremove", temp_registry)
    assert get_command("toremove", temp_registry) is None


def test_remove_nonexistent_command(temp_registry: Path):
    """Test that removing a nonexistent command raises an error."""
    with pytest.raises(UnknownCommandError):
        remove_command("nonexistent", temp_registry)


def test_rename_command(temp_registry: Path):
    """Test renaming a command."""
    cmd = RegisteredCommand(
        name="oldname",
        type="shell",
        target="echo test",
    )

    add_command(cmd, temp_registry)
    rename_command("oldname", "newname", temp_registry)

    commands = load_registry(temp_registry)
    assert "oldname" not in commands
    assert "newname" in commands
    assert commands["newname"].target == "echo test"


def test_rename_to_existing_name(temp_registry: Path):
    """Test that renaming to an existing name raises an error."""
    cmd1 = RegisteredCommand(name="cmd1", type="shell", target="echo 1")
    cmd2 = RegisteredCommand(name="cmd2", type="shell", target="echo 2")

    add_command(cmd1, temp_registry)
    add_command(cmd2, temp_registry)

    with pytest.raises(NameCollisionError):
        rename_command("cmd1", "cmd2", temp_registry)


def test_rename_nonexistent_command(temp_registry: Path):
    """Test that renaming a nonexistent command raises an error."""
    with pytest.raises(UnknownCommandError):
        rename_command("nonexistent", "newname", temp_registry)


def test_list_commands(temp_registry: Path):
    """Test listing commands."""
    cmd1 = RegisteredCommand(name="cmd1", type="shell", target="echo 1")
    cmd2 = RegisteredCommand(name="cmd2", type="shell", target="echo 2")
    cmd3 = RegisteredCommand(name="other", type="shell", target="echo 3")

    add_command(cmd1, temp_registry)
    add_command(cmd2, temp_registry)
    add_command(cmd3, temp_registry)

    # List all
    all_commands = list_commands(path=temp_registry)
    assert len(all_commands) == 3

    # List with pattern
    filtered = list_commands(pattern="cmd", path=temp_registry)
    assert len(filtered) == 2
    assert all("cmd" in c.name for c in filtered)


def test_get_command(temp_registry: Path):
    """Test getting a specific command."""
    cmd = RegisteredCommand(name="mycommand", type="shell", target="echo test")
    add_command(cmd, temp_registry)

    retrieved = get_command("mycommand", temp_registry)
    assert retrieved is not None
    assert retrieved.name == "mycommand"

    nonexistent = get_command("nonexistent", temp_registry)
    assert nonexistent is None
