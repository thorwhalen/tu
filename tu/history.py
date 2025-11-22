"""Command execution history tracking."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import HistoryEntry


def get_history_path() -> Path:
    """Get the path to the history file.

    Returns:
        Path to the history JSON file.
    """
    # Use XDG data directory
    data_dir = Path.home() / ".local" / "share" / "tu"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "history.json"


def load_history(path: Optional[Path] = None, limit: Optional[int] = None) -> list[HistoryEntry]:
    """Load command execution history.

    Args:
        path: Optional path to history file.
        limit: Optional limit on number of entries to load (most recent first).

    Returns:
        List of HistoryEntry objects, ordered from most recent to oldest.
    """
    if path is None:
        path = get_history_path()

    if not path.exists():
        return []

    try:
        with open(path, "r") as f:
            data = json.load(f)

        entries = [HistoryEntry.from_dict(entry) for entry in data.get("entries", [])]

        # Sort by executed_at, most recent first
        entries.sort(key=lambda e: e.executed_at, reverse=True)

        if limit is not None:
            entries = entries[:limit]

        return entries

    except (json.JSONDecodeError, KeyError):
        # If history is corrupted, return empty list
        return []


def save_history(entries: list[HistoryEntry], path: Optional[Path] = None) -> None:
    """Save command execution history.

    Args:
        entries: List of HistoryEntry objects.
        path: Optional path to history file.
    """
    if path is None:
        path = get_history_path()

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "entries": [entry.to_dict() for entry in entries]
    }

    # Atomic write
    temp_path = path.with_suffix(".tmp")
    try:
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2)
        temp_path.replace(path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise


def add_history_entry(entry: HistoryEntry, max_entries: int = 1000) -> None:
    """Add an entry to command history.

    Args:
        entry: HistoryEntry to add.
        max_entries: Maximum number of entries to keep (oldest removed first).
    """
    entries = load_history()
    entries.insert(0, entry)  # Add to front (most recent)

    # Keep only the most recent max_entries
    if len(entries) > max_entries:
        entries = entries[:max_entries]

    save_history(entries)


def get_command_history(
    command_name: str,
    limit: Optional[int] = None
) -> list[HistoryEntry]:
    """Get history for a specific command.

    Args:
        command_name: Name of the command to get history for.
        limit: Optional limit on number of entries.

    Returns:
        List of HistoryEntry objects for the specified command.
    """
    all_entries = load_history()

    # Filter by command name
    filtered = [e for e in all_entries if e.command_name == command_name]

    if limit is not None:
        filtered = filtered[:limit]

    return filtered


def clear_history() -> None:
    """Clear all command history."""
    path = get_history_path()
    if path.exists():
        path.unlink()
