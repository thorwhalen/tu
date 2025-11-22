"""Integration tests for the CLI."""

import sys
from io import StringIO

import pytest

from tu.cli import main


def test_cli_help(monkeypatch):
    """Test the --help flag."""
    # Capture help output
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0


def test_cli_list_empty(temp_registry, monkeypatch, capsys):
    """Test listing commands when registry is empty."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    exit_code = main(["--list"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "No commands registered" in captured.out


def test_cli_register_and_list(temp_registry, monkeypatch, capsys):
    """Test registering a command and listing it."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Register a command
    exit_code = main([
        "--register",
        "--name", "test",
        "--type", "shell",
        "--description", "Test command",
        "echo hello"
    ])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Registered command 'test'" in captured.out

    # List commands
    exit_code = main(["--list"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "test" in captured.out
    assert "Test command" in captured.out


def test_cli_show_command(temp_registry, monkeypatch, capsys):
    """Test showing command details."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Register a command first
    main([
        "--register",
        "--name", "mycommand",
        "--type", "shell",
        "--description", "My test command",
        "echo test"
    ])

    # Show the command
    exit_code = main(["--show", "mycommand"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Name: mycommand" in captured.out
    assert "Type: shell" in captured.out
    assert "Target: echo test" in captured.out
    assert "Description: My test command" in captured.out


def test_cli_unregister(temp_registry, monkeypatch, capsys):
    """Test unregistering a command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Register and then unregister
    main(["--register", "--name", "temp", "echo test"])
    exit_code = main(["--unregister", "temp"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Unregistered command 'temp'" in captured.out


def test_cli_rename(temp_registry, monkeypatch, capsys):
    """Test renaming a command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Register and then rename
    main(["--register", "--name", "old", "echo test"])
    exit_code = main(["--rename", "old", "new"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Renamed command 'old' to 'new'" in captured.out


def test_cli_run_command(temp_registry, monkeypatch, capsys):
    """Test running a registered command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Register a command
    main(["--register", "--name", "greet", "--type", "shell", "echo"])

    # Run the command
    exit_code = main(["greet", "hello"])
    assert exit_code == 0


def test_cli_run_unknown_command(temp_registry, monkeypatch, capsys):
    """Test running an unknown command."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    exit_code = main(["nonexistent"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Unknown command" in captured.err


def test_cli_completion(temp_registry, monkeypatch, capsys):
    """Test shell completion."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    # Register some commands
    main(["--register", "--name", "cmd1", "echo 1"])
    main(["--register", "--name", "cmd2", "echo 2"])
    main(["--register", "--name", "other", "echo 3"])

    # Clear captured output from registration
    capsys.readouterr()

    # Test completion
    exit_code = main(["--complete", "cmd"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "cmd1" in captured.out
    assert "cmd2" in captured.out
    assert "other" not in captured.out


def test_cli_completion_script(capsys):
    """Test getting completion script."""
    exit_code = main(["--completion-script", "bash"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "_tu_completion" in captured.out


def test_cli_install_completion(capsys):
    """Test install completion instructions."""
    exit_code = main(["--install-completion", "bash"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "bashrc" in captured.out.lower()


def test_cli_register_with_tags(temp_registry, monkeypatch, capsys):
    """Test registering a command with tags."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    exit_code = main([
        "--register",
        "--name", "tagged",
        "--tags", "build,test",
        "echo hello"
    ])
    assert exit_code == 0

    # Show command to verify tags
    main(["--show", "tagged"])
    captured = capsys.readouterr()
    assert "build" in captured.out
    assert "test" in captured.out


def test_cli_no_args_shows_list(temp_registry, monkeypatch, capsys):
    """Test that no arguments shows the list."""
    monkeypatch.setattr("tu.registry.get_registry_path", lambda: temp_registry)

    exit_code = main([])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "No commands registered" in captured.out
