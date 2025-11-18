"""Pytest configuration and fixtures."""

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_registry() -> Generator[Path, None, None]:
    """Create a temporary registry file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        registry_path = Path(f.name)
        # Initialize with empty registry
        json.dump({"version": 1, "commands": {}}, f)

    yield registry_path

    # Cleanup
    if registry_path.exists():
        registry_path.unlink()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
