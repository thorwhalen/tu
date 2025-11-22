"""Tests for the resolve module."""

import pytest

from tu.exceptions import InvalidNameError
from tu.models import RegisteredCommand
from tu.registry import add_command, get_command, list_commands as _list_commands
from tu.resolve import (
    infer_command_type,
    infer_default_name,
    is_dotted_name,
    resolve_command,
    suggest_commands,
    validate_name,
)


def test_is_dotted_name():
    """Test dotted name detection."""
    assert is_dotted_name("mypackage.mymodule")
    assert is_dotted_name("a.b.c")
    assert not is_dotted_name("simple")
    assert not is_dotted_name("my:namespace:cmd")


def test_validate_name():
    """Test name validation."""
    # Valid names
    validate_name("simple")
    validate_name("my:namespace:cmd")
    validate_name("my-command")
    validate_name("my_command")
    validate_name("my.module")

    # Invalid names
    with pytest.raises(InvalidNameError):
        validate_name("")

    with pytest.raises(InvalidNameError):
        validate_name("my::command")  # Double colons

    with pytest.raises(InvalidNameError):
        validate_name(":command")  # Leading colon

    with pytest.raises(InvalidNameError):
        validate_name("command:")  # Trailing colon

    with pytest.raises(InvalidNameError):
        validate_name("my command")  # Space


def test_infer_command_type():
    """Test command type inference."""
    # Python callable
    assert infer_command_type("mymodule:main") == "python_callable"
    assert infer_command_type("package.module:function") == "python_callable"

    # Python module
    assert infer_command_type("mypackage.mymodule") == "python_module"
    assert infer_command_type("a.b.c") == "python_module"

    # Shell
    assert infer_command_type("ls") == "shell"
    assert infer_command_type("echo hello") == "shell"
    assert infer_command_type("/usr/bin/ls") == "shell"


def test_infer_default_name():
    """Test default name inference."""
    # Python module
    assert infer_default_name("mypackage.mymodule", "python_module") == "mymodule"
    assert infer_default_name("a.b.c", "python_module") == "c"

    # Python callable
    assert infer_default_name("mymodule:main", "python_callable") == "main"
    assert infer_default_name("pkg.mod:func", "python_callable") == "func"

    # Shell
    assert infer_default_name("ls", "shell") == "ls"
    assert infer_default_name("/usr/bin/ffmpeg", "shell") == "ffmpeg"
    assert infer_default_name("echo hello", "shell") == "echo"


def test_resolve_command(temp_registry, monkeypatch):
    """Test command resolution."""
    monkeypatch.setattr("tu.resolve.get_command", lambda name: get_command(name, temp_registry))

    # Add a command to the registry
    cmd = RegisteredCommand(
        name="mycommand",
        type="shell",
        target="echo test"
    )
    add_command(cmd, temp_registry)

    # Resolve registered command
    resolved, is_dotted = resolve_command("mycommand")
    assert resolved is not None
    assert resolved.name == "mycommand"
    assert not is_dotted

    # Resolve dotted name (not registered)
    resolved, is_dotted = resolve_command("mypackage.mymodule")
    assert resolved is None
    assert is_dotted

    # Resolve unknown command
    resolved, is_dotted = resolve_command("unknown")
    assert resolved is None
    assert not is_dotted


def test_suggest_commands(temp_registry, monkeypatch):
    """Test command suggestions."""
    monkeypatch.setattr("tu.resolve.list_commands", lambda: _list_commands(path=temp_registry))

    # Add some commands
    for name in ["clean", "build", "deploy", "test"]:
        cmd = RegisteredCommand(name=name, type="shell", target=f"echo {name}")
        add_command(cmd, temp_registry)

    # Test suggestions
    suggestions = suggest_commands("clen")
    assert "clean" in suggestions

    suggestions = suggest_commands("bild")
    assert "build" in suggestions

    # No suggestions for very different names
    suggestions = suggest_commands("xyz")
    assert len(suggestions) == 0
