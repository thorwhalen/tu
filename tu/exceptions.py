"""Custom exceptions for the tu package."""


class TuError(Exception):
    """Base exception for all tu errors."""
    pass


class UnknownCommandError(TuError):
    """Raised when a command is not found in the registry."""
    pass


class NameCollisionError(TuError):
    """Raised when attempting to register a command with an existing name."""
    pass


class RegistryCorruptedError(TuError):
    """Raised when the registry file is corrupted or invalid."""
    pass


class InvalidCommandTypeError(TuError):
    """Raised when an invalid command type is specified."""
    pass


class InvalidNameError(TuError):
    """Raised when a command name is invalid."""
    pass


class CommandExecutionError(TuError):
    """Raised when a command fails to execute."""
    pass
