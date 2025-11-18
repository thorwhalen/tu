"""Command execution for tu."""

import importlib
import os
import subprocess
import sys
import time
from typing import Optional

from .exceptions import CommandExecutionError
from .models import ExecutionPlan, RunResult


def execute_shell(
    target: str,
    args: list[str],
    cwd: Optional[str] = None,
    env: Optional[dict[str, str]] = None,
    capture_output: bool = False,
    timeout: Optional[int] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> RunResult:
    """Execute a shell command.

    Args:
        target: Shell command or path to execute.
        args: Arguments to pass to the command.
        cwd: Working directory for execution.
        env: Environment variables.
        capture_output: Whether to capture stdout/stderr.
        timeout: Timeout in seconds.
        dry_run: If True, show what would execute without running.
        verbose: If True, show detailed execution information.

    Returns:
        RunResult with execution results.

    Raises:
        CommandExecutionError: If execution fails.
    """
    # Build the full command
    if " " in target:
        # Shell command with arguments
        cmd_str = f"{target} {' '.join(args)}" if args else target
        cmd_for_display = cmd_str
        use_shell = True
        cmd_for_exec = cmd_str
    else:
        # Simple command or path
        cmd_for_exec = [target] + args
        cmd_for_display = " ".join([target] + args)
        use_shell = False

    if dry_run:
        print(f"[DRY RUN] Would execute: {cmd_for_display}")
        if cwd:
            print(f"[DRY RUN]   Working directory: {cwd}")
        if env:
            print(f"[DRY RUN]   Environment variables: {env}")
        if timeout:
            print(f"[DRY RUN]   Timeout: {timeout}s")
        return RunResult(returncode=0, duration=0.0)

    if verbose:
        print(f"[VERBOSE] Executing: {cmd_for_display}")
        if cwd:
            print(f"[VERBOSE]   Working directory: {cwd}")
        if env:
            print(f"[VERBOSE]   Environment variables: {env}")
        if timeout:
            print(f"[VERBOSE]   Timeout: {timeout}s")

    try:
        start_time = time.time()

        result = subprocess.run(
            cmd_for_exec,
            shell=use_shell,
            cwd=cwd,
            env=env,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )

        duration = time.time() - start_time

        if verbose:
            print(f"[VERBOSE] Completed in {duration:.2f}s with exit code {result.returncode}")

        return RunResult(
            returncode=result.returncode,
            stdout=result.stdout if capture_output else None,
            stderr=result.stderr if capture_output else None,
            duration=duration
        )

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        raise CommandExecutionError(
            f"Command timed out after {timeout}s: {cmd_for_display}"
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
    capture_output: bool = False,
    timeout: Optional[int] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> RunResult:
    """Execute a Python module using python -m.

    Args:
        module: Python module to execute.
        args: Arguments to pass to the module.
        cwd: Working directory for execution.
        env: Environment variables.
        capture_output: Whether to capture stdout/stderr.
        timeout: Timeout in seconds.
        dry_run: If True, show what would execute without running.
        verbose: If True, show detailed execution information.

    Returns:
        RunResult with execution results.

    Raises:
        CommandExecutionError: If execution fails.
    """
    cmd = [sys.executable, "-m", module] + args
    cmd_for_display = " ".join(cmd)

    if dry_run:
        print(f"[DRY RUN] Would execute: {cmd_for_display}")
        if cwd:
            print(f"[DRY RUN]   Working directory: {cwd}")
        if env:
            print(f"[DRY RUN]   Environment variables: {env}")
        if timeout:
            print(f"[DRY RUN]   Timeout: {timeout}s")
        return RunResult(returncode=0, duration=0.0)

    if verbose:
        print(f"[VERBOSE] Executing: {cmd_for_display}")
        if cwd:
            print(f"[VERBOSE]   Working directory: {cwd}")
        if env:
            print(f"[VERBOSE]   Environment variables: {env}")
        if timeout:
            print(f"[VERBOSE]   Timeout: {timeout}s")

    try:
        start_time = time.time()

        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )

        duration = time.time() - start_time

        if verbose:
            print(f"[VERBOSE] Completed in {duration:.2f}s with exit code {result.returncode}")

        return RunResult(
            returncode=result.returncode,
            stdout=result.stdout if capture_output else None,
            stderr=result.stderr if capture_output else None,
            duration=duration
        )

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        raise CommandExecutionError(
            f"Command timed out after {timeout}s: {cmd_for_display}"
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
    capture_output: bool = False,
    timeout: Optional[int] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> RunResult:
    """Execute a Python callable.

    Args:
        target: Module:function string (e.g., "mymodule:main").
        args: Arguments to pass to the callable.
        cwd: Working directory (changes sys.path and os.cwd if provided).
        env: Environment variables (updates os.environ if provided).
        capture_output: Whether to capture stdout/stderr.
        timeout: Timeout in seconds (not supported for callables).
        dry_run: If True, show what would execute without running.
        verbose: If True, show detailed execution information.

    Returns:
        RunResult with execution results.

    Raises:
        CommandExecutionError: If execution fails.
    """
    if ":" not in target:
        raise CommandExecutionError(
            f"Invalid callable target '{target}'. "
            "Expected format: module:function"
        )

    module_path, function_name = target.rsplit(":", 1)

    if dry_run:
        print(f"[DRY RUN] Would execute: {target}({args})")
        if cwd:
            print(f"[DRY RUN]   Working directory: {cwd}")
        if env:
            print(f"[DRY RUN]   Environment variables: {env}")
        return RunResult(returncode=0, duration=0.0)

    if verbose:
        print(f"[VERBOSE] Executing: {target}({args})")
        if cwd:
            print(f"[VERBOSE]   Working directory: {cwd}")
        if env:
            print(f"[VERBOSE]   Environment variables: {env}")

    try:
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
            start_time = time.time()

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

            duration = time.time() - start_time

            # Interpret result as return code
            if result is None:
                returncode = 0
            elif isinstance(result, int):
                returncode = result
            else:
                returncode = 0  # Treat non-integer returns as success

            if verbose:
                print(f"[VERBOSE] Completed in {duration:.2f}s with exit code {returncode}")

            return RunResult(
                returncode=returncode,
                stdout=stdout_str,
                stderr=stderr_str,
                duration=duration
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
            capture_output=capture_output,
            timeout=plan.timeout,
            dry_run=plan.dry_run,
            verbose=plan.verbose
        )
    elif plan.command_type == "python_module":
        return execute_python_module(
            plan.target,
            plan.args,
            cwd=plan.cwd,
            env=plan.env,
            capture_output=capture_output,
            timeout=plan.timeout,
            dry_run=plan.dry_run,
            verbose=plan.verbose
        )
    elif plan.command_type == "python_callable":
        return execute_python_callable(
            plan.target,
            plan.args,
            cwd=plan.cwd,
            env=plan.env,
            capture_output=capture_output,
            timeout=plan.timeout,
            dry_run=plan.dry_run,
            verbose=plan.verbose
        )
    else:
        raise CommandExecutionError(
            f"Unknown command type: {plan.command_type}"
        )
