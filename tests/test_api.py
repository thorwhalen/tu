"""Tests for the Python API."""

import pytest

from tu import api
from tu.exceptions import InvalidNameError, NameCollisionError, UnknownCommandError
from tu.models import RegisteredCommand


def test_register_and_list_commands(temp_registry, monkeypatch):
    """Test registering and listing commands."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Initially empty
    commands = api.list_commands()
    assert len(commands) == 0

    # Register a command
    cmd = api.register_command(
        target="echo hello",
        name="greet",
        type="shell",
        description="Greet the user"
    )
    assert cmd.name == "greet"
    assert cmd.type == "shell"

    # List again
    commands = api.list_commands()
    assert len(commands) == 1
    assert commands[0].name == "greet"


def test_register_command_with_inference(temp_registry, monkeypatch):
    """Test registering a command with type and name inference."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Python module - should infer type and name
    cmd = api.register_command(target="mypackage.mymodule")
    assert cmd.name == "mymodule"
    assert cmd.type == "python_module"

    # Clean up for next test
    api.unregister_command("mymodule")

    # Python callable
    cmd = api.register_command(target="mypackage.module:function")
    assert cmd.name == "function"
    assert cmd.type == "python_callable"


def test_register_duplicate_command(temp_registry, monkeypatch):
    """Test that registering a duplicate command fails."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    api.register_command(target="echo test", name="test", type="shell")

    with pytest.raises(NameCollisionError):
        api.register_command(target="echo test2", name="test", type="shell")


def test_register_dotted_name_without_allow(temp_registry, monkeypatch):
    """Test that registering a dotted name without allow_dot_name fails."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    with pytest.raises(InvalidNameError, match="dotted-name rule"):
        api.register_command(target="echo test", name="my.command")


def test_register_dotted_name_with_allow(temp_registry, monkeypatch):
    """Test registering a dotted name with allow_dot_name."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    cmd = api.register_command(
        target="echo test",
        name="my.command",
        allow_dot_name=True
    )
    assert cmd.name == "my.command"


def test_unregister_command(temp_registry, monkeypatch):
    """Test unregistering a command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    api.register_command(target="echo test", name="test")
    assert api.get_command_info("test") is not None

    api.unregister_command("test")
    assert api.get_command_info("test") is None


def test_unregister_nonexistent_command(temp_registry, monkeypatch):
    """Test unregistering a nonexistent command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    with pytest.raises(UnknownCommandError):
        api.unregister_command("nonexistent")


def test_rename_command(temp_registry, monkeypatch):
    """Test renaming a command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    api.register_command(target="echo test", name="old")
    api.rename_command("old", "new")

    assert api.get_command_info("old") is None
    assert api.get_command_info("new") is not None


def test_get_command_info(temp_registry, monkeypatch):
    """Test getting command info."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    api.register_command(
        target="echo test",
        name="mycommand",
        description="Test command",
        tags=["test", "demo"]
    )

    cmd = api.get_command_info("mycommand")
    assert cmd is not None
    assert cmd.name == "mycommand"
    assert cmd.description == "Test command"
    assert "test" in cmd.tags


def test_run_shell_command(temp_registry, monkeypatch):
    """Test running a shell command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    api.register_command(target="echo", name="echo_cmd", type="shell")

    result = api.run("echo_cmd", args=["hello"], capture_output=True)
    assert result.returncode == 0
    assert "hello" in result.stdout


def test_run_dotted_name(temp_registry, monkeypatch):
    """Test running a dotted name (Python module)."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Run json.tool (should work even though not registered)
    result = api.run("json.tool", args=[], capture_output=True)
    # Just check it executes
    assert result.returncode is not None


def test_run_unknown_command(temp_registry, monkeypatch):
    """Test running an unknown command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    with pytest.raises(UnknownCommandError):
        api.run("nonexistent")


def test_list_commands_with_pattern(temp_registry, monkeypatch):
    """Test listing commands with a pattern filter."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    api.register_command(target="echo 1", name="cmd1")
    api.register_command(target="echo 2", name="cmd2")
    api.register_command(target="echo 3", name="other")

    # Filter by pattern
    commands = api.list_commands(pattern="cmd")
    assert len(commands) == 2
    assert all("cmd" in c.name for c in commands)
