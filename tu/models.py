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
        aliases: List of alternative names for this command
        depends_on: List of command names that must run before this one
        env: Environment variables to set when running this command
        timeout: Timeout in seconds for command execution
    """
    name: str
    type: CommandType
    target: str
    description: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    aliases: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    timeout: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = {
            "type": self.type,
            "target": self.target,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        # Only include optional fields if they have values
        if self.aliases:
            data["aliases"] = self.aliases
        if self.depends_on:
            data["depends_on"] = self.depends_on
        if self.env:
            data["env"] = self.env
        if self.timeout is not None:
            data["timeout"] = self.timeout
        return data

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
            aliases=data.get("aliases", []),
            depends_on=data.get("depends_on", []),
            env=data.get("env", {}),
            timeout=data.get("timeout"),
        )


@dataclass
class RunResult:
    """Result of running a command.

    Attributes:
        returncode: Exit code from the command
        stdout: Captured stdout (if requested)
        stderr: Captured stderr (if requested)
        duration: Execution duration in seconds
    """
    returncode: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    duration: Optional[float] = None


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
        timeout: Timeout in seconds
        dry_run: If True, show what would execute without running
        verbose: If True, show detailed execution information
    """
    command_type: CommandType
    target: str
    args: list[str] = field(default_factory=list)
    cwd: Optional[str] = None
    env: Optional[dict[str, str]] = None
    timeout: Optional[int] = None
    dry_run: bool = False
    verbose: bool = False


@dataclass
class HistoryEntry:
    """Entry in command execution history.

    Attributes:
        command_name: Name of the command that was executed
        args: Arguments passed to the command
        returncode: Exit code from execution
        executed_at: Timestamp of execution
        duration: Execution duration in seconds
        cwd: Working directory at execution time
    """
    command_name: str
    args: list[str]
    returncode: int
    executed_at: datetime
    duration: float
    cwd: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "command_name": self.command_name,
            "args": self.args,
            "returncode": self.returncode,
            "executed_at": self.executed_at.isoformat(),
            "duration": self.duration,
            "cwd": self.cwd,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "HistoryEntry":
        """Create from dictionary during JSON deserialization."""
        return cls(
            command_name=data["command_name"],
            args=data["args"],
            returncode=data["returncode"],
            executed_at=datetime.fromisoformat(data["executed_at"]),
            duration=data["duration"],
            cwd=data.get("cwd"),
        )
