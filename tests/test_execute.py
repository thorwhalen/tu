"""Tests for the execute module."""

import sys
from pathlib import Path

import pytest

from tu.execute import (
    execute_plan,
    execute_python_callable,
    execute_python_module,
    execute_shell,
)
from tu.models import ExecutionPlan


def test_execute_shell_simple():
    """Test executing a simple shell command."""
    result = execute_shell("echo", ["hello"], capture_output=True)
    assert result.returncode == 0
    assert "hello" in result.stdout


def test_execute_shell_with_args():
    """Test executing a shell command with arguments."""
    result = execute_shell("echo", ["hello", "world"], capture_output=True)
    assert result.returncode == 0
    assert "hello world" in result.stdout


def test_execute_shell_failure():
    """Test executing a shell command that fails."""
    result = execute_shell("false", [], capture_output=True)
    assert result.returncode != 0


def test_execute_python_module():
    """Test executing a Python module."""
    # Execute python -m json.tool with JSON input
    result = execute_python_module(
        "json.tool",
        [],
        capture_output=True
    )
    # json.tool without input will fail, but we're just testing it runs
    assert result.returncode is not None


def test_execute_python_callable(temp_dir: Path):
    """Test executing a Python callable."""
    # Create a test module
    module_path = temp_dir / "test_module.py"
    module_path.write_text("""
def test_func(args):
    print(f"Args: {args}")
    return 0

def failing_func(args):
    return 1

def no_return_func(args):
    pass
""")

    # Add temp_dir to sys.path
    sys.path.insert(0, str(temp_dir))

    try:
        # Test successful execution
        result = execute_python_callable(
            "test_module:test_func",
            ["arg1", "arg2"],
            capture_output=True
        )
        assert result.returncode == 0
        assert "Args:" in result.stdout

        # Test failing function
        result = execute_python_callable(
            "test_module:failing_func",
            [],
            capture_output=True
        )
        assert result.returncode == 1

        # Test function with no return (should default to 0)
        result = execute_python_callable(
            "test_module:no_return_func",
            [],
            capture_output=True
        )
        assert result.returncode == 0

    finally:
        sys.path.remove(str(temp_dir))


def test_execute_plan_shell():
    """Test executing an ExecutionPlan with shell command."""
    plan = ExecutionPlan(
        command_type="shell",
        target="echo",
        args=["test"]
    )
    result = execute_plan(plan, capture_output=True)
    assert result.returncode == 0
    assert "test" in result.stdout


def test_execute_plan_python_module():
    """Test executing an ExecutionPlan with Python module."""
    plan = ExecutionPlan(
        command_type="python_module",
        target="json.tool",
        args=[]
    )
    result = execute_plan(plan, capture_output=True)
    # Just check it executes
    assert result.returncode is not None


def test_execute_shell_with_cwd(temp_dir: Path):
    """Test executing a shell command with a specific working directory."""
    # Create a test file in temp_dir
    test_file = temp_dir / "test.txt"
    test_file.write_text("test content")

    # Execute ls in temp_dir
    result = execute_shell("ls", [], cwd=str(temp_dir), capture_output=True)
    assert result.returncode == 0
    assert "test.txt" in result.stdout
