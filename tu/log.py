"""Command output logging for tu."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import RunResult


def get_log_directory() -> Path:
    """Get the default log directory.

    Returns:
        Path to the log directory.
    """
    # Use XDG data directory
    log_dir = Path.home() / ".local" / "share" / "tu" / "logs"
    return log_dir


def write_log(
    command_name: str,
    result: RunResult,
    args: list[str],
    log_dir: Optional[Path] = None
) -> Path:
    """Write command output to a log file.

    Args:
        command_name: Name of the command that was executed.
        result: RunResult from execution.
        args: Arguments passed to the command.
        log_dir: Optional log directory. If None, uses default.

    Returns:
        Path to the log file that was written.
    """
    if log_dir is None:
        log_dir = get_log_directory()

    # Ensure log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = command_name.replace(":", "_").replace("/", "_")
    log_file = log_dir / f"{safe_name}_{timestamp}.log"

    # Write log
    with open(log_file, "w") as f:
        f.write(f"Command: {command_name}\n")
        if args:
            f.write(f"Arguments: {' '.join(args)}\n")
        f.write(f"Executed at: {datetime.now().isoformat()}\n")
        f.write(f"Exit code: {result.returncode}\n")
        if result.duration:
            f.write(f"Duration: {result.duration:.2f}s\n")
        f.write("\n")

        if result.stdout:
            f.write("=== STDOUT ===\n")
            f.write(result.stdout)
            f.write("\n")

        if result.stderr:
            f.write("=== STDERR ===\n")
            f.write(result.stderr)
            f.write("\n")

    return log_file


def get_recent_logs(command_name: Optional[str] = None, limit: int = 10) -> list[Path]:
    """Get recent log files.

    Args:
        command_name: Optional command name to filter by.
        limit: Maximum number of log files to return.

    Returns:
        List of log file paths, ordered by modification time (most recent first).
    """
    log_dir = get_log_directory()

    if not log_dir.exists():
        return []

    # Get all log files
    if command_name:
        safe_name = command_name.replace(":", "_").replace("/", "_")
        pattern = f"{safe_name}_*.log"
    else:
        pattern = "*.log"

    log_files = list(log_dir.glob(pattern))

    # Sort by modification time, most recent first
    log_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    return log_files[:limit]


def clear_old_logs(days: int = 30) -> int:
    """Clear log files older than specified days.

    Args:
        days: Number of days to keep logs for.

    Returns:
        Number of log files deleted.
    """
    log_dir = get_log_directory()

    if not log_dir.exists():
        return 0

    cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
    deleted = 0

    for log_file in log_dir.glob("*.log"):
        if log_file.stat().st_mtime < cutoff_time:
            log_file.unlink()
            deleted += 1

    return deleted
