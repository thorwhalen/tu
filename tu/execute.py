"""Command execution for tu."""

import importlib
import subprocess
import sys
from typing import Optional

from .exceptions import CommandExecutionError
from .models import ExecutionPlan, RunResult


def execute_shell(
    target: str,
    args: list[str],
    cwd: Optional[str] = None,
    env: Optional[dict[str, str]] = None,
    capture_output: bool = False
) -> RunResult:
    """Execute a shell command.

    Args:
        target: Shell command or path to execute.
        args: Arguments to pass to the command.
        cwd: Working directory for execution.
        env: Environment variables.
        capture_output: Whether to capture stdout/stderr.

    Returns:
        RunResult with execution results.

    Raises:
        CommandExecutionError: If execution fails.
    """
    try:
        # Build the full command
        # If target contains spaces, treat it as a complete command
        if " " in target:
            # Shell command with arguments
            cmd = f"{target} {' '.join(args)}" if args else target
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                env=env,
                capture_output=capture_output,
                text=True
            )
        else:
            # Simple command or path
            cmd = [target] + args
            result = subprocess.run(
                cmd,
                shell=False,
                cwd=cwd,
                env=env,
                capture_output=capture_output,
                text=True
            )

        return RunResult(
            returncode=result.returncode,
            stdout=result.stdout if capture_output else None,
            stderr=result.stderr if capture_output else None
        )

    except FileNotFoundError:
        raise CommandExecutionError(
            f"Command not found: {target}"
        )
    except Exception as e:
        raise CommandExecutionError(
            f"Failed to execute shell command: {e}"
        )


def execute_python_module(
    module: str,
    args: list[str],
    cwd: Optional[str] = None,
    env: Optional[dict[str, str]] = None,
    capture_output: bool = False
) -> RunResult:
    """Execute a Python module using python -m.

    Args:
        module: Python module to execute.
        args: Arguments to pass to the module.
        cwd: Working directory for execution.
        env: Environment variables.
        capture_output: Whether to capture stdout/stderr.

    Returns:
        RunResult with execution results.

    Raises:
        CommandExecutionError: If execution fails.
    """
    try:
        cmd = [sys.executable, "-m", module] + args
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=capture_output,
            text=True
        )

        return RunResult(
            returncode=result.returncode,
            stdout=result.stdout if capture_output else None,
            stderr=result.stderr if capture_output else None
        )

    except Exception as e:
        raise CommandExecutionError(
            f"Failed to execute Python module '{module}': {e}"
        )


def execute_python_callable(
    target: str,
    args: list[str],
    cwd: Optional[str] = None,
    env: Optional[dict[str, str]] = None,
    capture_output: bool = False
) -> RunResult:
    """Execute a Python callable.

    Args:
        target: Module:function string (e.g., "mymodule:main").
        args: Arguments to pass to the callable.
        cwd: Working directory (changes sys.path and os.cwd if provided).
        env: Environment variables (updates os.environ if provided).
        capture_output: Whether to capture stdout/stderr.

    Returns:
        RunResult with execution results.

    Raises:
        CommandExecutionError: If execution fails.
    """
    try:
        # Parse module:function
        if ":" not in target:
            raise CommandExecutionError(
                f"Invalid callable target '{target}'. "
                "Expected format: module:function"
            )

        module_path, function_name = target.rsplit(":", 1)

        # Import the module
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise CommandExecutionError(
                f"Failed to import module '{module_path}': {e}"
            )

        # Get the function
        if not hasattr(module, function_name):
            raise CommandExecutionError(
                f"Module '{module_path}' has no attribute '{function_name}'"
            )

        func = getattr(module, function_name)

        if not callable(func):
            raise CommandExecutionError(
                f"'{target}' is not callable"
            )

        # Handle cwd and env if needed
        import os
        old_cwd = None
        old_env = {}

        if cwd:
            old_cwd = os.getcwd()
            os.chdir(cwd)

        if env:
            # Save and update environment
            for key, value in env.items():
                old_env[key] = os.environ.get(key)
                os.environ[key] = value

        try:
            # Capture output if requested
            if capture_output:
                import io
                from contextlib import redirect_stdout, redirect_stderr

                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()

                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    result = func(args)

                stdout_str = stdout_capture.getvalue()
                stderr_str = stderr_capture.getvalue()
            else:
                result = func(args)
                stdout_str = None
                stderr_str = None

            # Interpret result as return code
            if result is None:
                returncode = 0
            elif isinstance(result, int):
                returncode = result
            else:
                returncode = 0  # Treat non-integer returns as success

            return RunResult(
                returncode=returncode,
                stdout=stdout_str,
                stderr=stderr_str
            )

        finally:
            # Restore cwd and env
            if old_cwd:
                os.chdir(old_cwd)
            if env:
                for key, old_value in old_env.items():
                    if old_value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = old_value

    except CommandExecutionError:
        raise
    except Exception as e:
        import traceback
        raise CommandExecutionError(
            f"Failed to execute callable '{target}': {e}\n"
            f"{traceback.format_exc()}"
        )


def execute_plan(plan: ExecutionPlan, capture_output: bool = False) -> RunResult:
    """Execute an ExecutionPlan.

    Args:
        plan: ExecutionPlan to execute.
        capture_output: Whether to capture stdout/stderr.

    Returns:
        RunResult with execution results.
    """
    if plan.command_type == "shell":
        return execute_shell(
            plan.target,
            plan.args,
            cwd=plan.cwd,
            env=plan.env,
            capture_output=capture_output
        )
    elif plan.command_type == "python_module":
        return execute_python_module(
            plan.target,
            plan.args,
            cwd=plan.cwd,
            env=plan.env,
            capture_output=capture_output
        )
    elif plan.command_type == "python_callable":
        return execute_python_callable(
            plan.target,
            plan.args,
            cwd=plan.cwd,
            env=plan.env,
            capture_output=capture_output
        )
    else:
        raise CommandExecutionError(
            f"Unknown command type: {plan.command_type}"
        )
