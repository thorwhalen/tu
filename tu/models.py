"""Data models for the tu package."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional


CommandType = Literal["shell", "python_module", "python_callable"]


@dataclass
class RegisteredCommand:
    """Represents a registered command in the tu registry.

    Attributes:
        name: Fully qualified name (FQN) of the command
        type: Type of command (shell, python_module, python_callable)
        target: The actual target to execute (command, module path, callable)
        description: Optional description of the command
        tags: List of tags for categorization
        created_at: Timestamp when the command was registered
        updated_at: Timestamp when the command was last updated
    """
    name: str
    type: CommandType
    target: str
    description: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "target": self.target,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "RegisteredCommand":
        """Create from dictionary during JSON deserialization."""
        return cls(
            name=name,
            type=data["type"],
            target=data["target"],
            description=data.get("description"),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
        )


@dataclass
class RunResult:
    """Result of running a command.

    Attributes:
        returncode: Exit code from the command
        stdout: Captured stdout (if requested)
        stderr: Captured stderr (if requested)
    """
    returncode: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None


@dataclass
class ExecutionPlan:
    """Plan for executing a command.

    This represents the execution context and is used by global options
    to transform command execution.

    Attributes:
        command_type: Type of command to execute
        target: The target to execute
        args: Arguments to pass to the command
        cwd: Working directory for execution
        env: Environment variables
    """
    command_type: CommandType
    target: str
    args: list[str] = field(default_factory=list)
    cwd: Optional[str] = None
    env: Optional[dict[str, str]] = None
