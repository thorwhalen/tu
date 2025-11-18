"""Command-line interface for tu."""

import argparse
import sys
from typing import Optional

from . import api
from .completion import get_completion_candidates, get_completion_script, install_completion
from .exceptions import InvalidNameError, NameCollisionError, TuError, UnknownCommandError
from .execute import execute_plan
from .models import ExecutionPlan
from .options import apply_global_options
from .registry import get_command, get_registry_path
from .resolve import is_dotted_name, resolve_command, suggest_commands
from .utils import (
    export_registry,
    get_registry_stats,
    import_registry,
    validate_all_commands,
    validate_command,
)


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    print(f"Error: {message}", file=sys.stderr)


def list_commands_cli(args: argparse.Namespace) -> int:
    """Handle the --list command."""
    try:
        commands = api.list_commands(pattern=args.filter)

        if not commands:
            if args.filter:
                print(f"No commands matching '{args.filter}' found.")
            else:
                print("No commands registered yet.")
                print("\nTo register a command:")
                print("  tu --register <target>")
            return 0

        # Group by namespace
        grouped: dict[str, list] = {}
        for cmd in commands:
            # Extract top-level namespace
            if ":" in cmd.name:
                namespace = cmd.name.split(":")[0]
            else:
                namespace = ""

            if namespace not in grouped:
                grouped[namespace] = []
            grouped[namespace].append(cmd)

        # Print grouped commands
        for namespace in sorted(grouped.keys()):
            if namespace:
                print(f"\n{namespace}:")
            for cmd in sorted(grouped[namespace], key=lambda c: c.name):
                desc = f" - {cmd.description}" if cmd.description else ""
                print(f"  {cmd.name}{desc}")

        return 0

    except Exception as e:
        print_error(str(e))
        return 1


def show_command_cli(args: argparse.Namespace) -> int:
    """Handle the --show command."""
    try:
        cmd = get_command(args.name)
        if cmd is None:
            print_error(f"Command '{args.name}' not found.")
            return 1

        print(f"Name: {cmd.name}")
        print(f"Type: {cmd.type}")
        print(f"Target: {cmd.target}")
        if cmd.description:
            print(f"Description: {cmd.description}")
        if cmd.tags:
            print(f"Tags: {', '.join(cmd.tags)}")
        print(f"Created: {cmd.created_at.isoformat()}")
        print(f"Updated: {cmd.updated_at.isoformat()}")

        return 0

    except Exception as e:
        print_error(str(e))
        return 1


def register_command_cli(args: argparse.Namespace) -> int:
    """Handle the --register command."""
    try:
        # Check for dotted name warning
        name_to_use = args.name if args.name else None
        if name_to_use and is_dotted_name(name_to_use) and not args.force_dot_name:
            print(
                f"Warning: Name '{name_to_use}' contains a dot, which conflicts with "
                "the dotted-name rule for Python modules."
            )
            print("If you proceed, the registered command will take precedence over the dotted-name rule.")
            response = input("Do you want to continue? [y/N] ")
            if response.lower() not in ["y", "yes"]:
                print("Registration cancelled.")
                return 0

        # Register the command
        allow_dot = args.force_dot_name or (name_to_use and is_dotted_name(name_to_use))
        cmd = api.register_command(
            target=args.target,
            name=args.name,
            type=args.type,
            description=args.description,
            tags=args.tags.split(",") if args.tags else None,
            allow_dot_name=allow_dot
        )

        print(f"Registered command '{cmd.name}' ({cmd.type}): {cmd.target}")
        return 0

    except (NameCollisionError, InvalidNameError) as e:
        print_error(str(e))
        return 1
    except Exception as e:
        print_error(f"Failed to register command: {e}")
        return 1


def unregister_command_cli(args: argparse.Namespace) -> int:
    """Handle the --unregister command."""
    try:
        api.unregister_command(args.name)
        print(f"Unregistered command '{args.name}'.")
        return 0

    except UnknownCommandError as e:
        print_error(str(e))
        return 1
    except Exception as e:
        print_error(f"Failed to unregister command: {e}")
        return 1


def rename_command_cli(args: argparse.Namespace) -> int:
    """Handle the --rename command."""
    try:
        api.rename_command(args.old_name, args.new_name)
        print(f"Renamed command '{args.old_name}' to '{args.new_name}'.")
        return 0

    except (UnknownCommandError, NameCollisionError, InvalidNameError) as e:
        print_error(str(e))
        return 1
    except Exception as e:
        print_error(f"Failed to rename command: {e}")
        return 1


def run_command_cli(args: argparse.Namespace) -> int:
    """Handle running a command."""
    try:
        name = args.command
        cmd_args = args.args

        # Resolve command
        command, is_dotted = resolve_command(name)

        if command is not None:
            # Execute registered command
            plan = ExecutionPlan(
                command_type=command.type,
                target=command.target,
                args=cmd_args
            )

            # Apply global options if any
            if args.subshell:
                from .options import subshell_option
                plan, _ = subshell_option(plan, [args.subshell])

            result = execute_plan(plan, capture_output=False)
            return result.returncode

        elif is_dotted:
            # Execute dotted name as Python module
            plan = ExecutionPlan(
                command_type="python_module",
                target=name,
                args=cmd_args
            )

            # Apply global options if any
            if args.subshell:
                from .options import subshell_option
                plan, _ = subshell_option(plan, [args.subshell])

            result = execute_plan(plan, capture_output=False)
            return result.returncode

        else:
            # Not found - suggest alternatives
            suggestions = suggest_commands(name)
            if suggestions:
                print_error(f"Unknown command: {name}")
                print("\nDid you mean one of these?", file=sys.stderr)
                for s in suggestions:
                    print(f"  - {s}", file=sys.stderr)
            else:
                print_error(f"Unknown command: {name}")
            return 1

    except TuError as e:
        print_error(str(e))
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def complete_cli(args: argparse.Namespace) -> int:
    """Handle the --complete command (for shell completion)."""
    try:
        candidates = get_completion_candidates(args.partial)
        for candidate in candidates:
            print(candidate)
        return 0
    except Exception:
        # Silently fail for completion
        return 0


def completion_script_cli(args: argparse.Namespace) -> int:
    """Handle the --completion-script command."""
    try:
        script = get_completion_script(args.shell)
        print(script)
        return 0
    except ValueError as e:
        print_error(str(e))
        return 1


def install_completion_cli(args: argparse.Namespace) -> int:
    """Handle the --install-completion command."""
    try:
        instructions = install_completion(args.shell)
        print(instructions)
        return 0
    except ValueError as e:
        print_error(str(e))
        return 1


def export_registry_cli(args: argparse.Namespace) -> int:
    """Handle the --export command."""
    try:
        from pathlib import Path
        export_registry(Path(args.export_path))
        print(f"Registry exported to {args.export_path}")
        return 0
    except Exception as e:
        print_error(f"Failed to export registry: {e}")
        return 1


def import_registry_cli(args: argparse.Namespace) -> int:
    """Handle the --import command."""
    try:
        from pathlib import Path
        import_registry(Path(args.import_path), merge=args.merge)
        if args.merge:
            print(f"Registry merged from {args.import_path}")
        else:
            print(f"Registry imported from {args.import_path}")
        return 0
    except Exception as e:
        print_error(f"Failed to import registry: {e}")
        return 1


def validate_cli(args: argparse.Namespace) -> int:
    """Handle the --validate command."""
    try:
        if args.validate_name:
            # Validate a specific command
            cmd = get_command(args.validate_name)
            if cmd is None:
                print_error(f"Command '{args.validate_name}' not found.")
                return 1

            is_valid, error = validate_command(cmd)
            if is_valid:
                print(f"Command '{args.validate_name}' is valid.")
                return 0
            else:
                print_error(f"Command '{args.validate_name}' is invalid: {error}")
                return 1
        else:
            # Validate all commands
            results = validate_all_commands()
            invalid = {name: error for name, error in results.items() if error is not None}

            if not invalid:
                print("All commands are valid.")
                return 0
            else:
                print("Invalid commands found:")
                for name, error in invalid.items():
                    print(f"  {name}: {error}")
                return 1

    except Exception as e:
        print_error(f"Validation failed: {e}")
        return 1


def stats_cli(args: argparse.Namespace) -> int:
    """Handle the --stats command."""
    try:
        stats = get_registry_stats()

        print(f"Total commands: {stats['total_commands']}")
        print(f"\nBy type:")
        for cmd_type, count in stats['by_type'].items():
            print(f"  {cmd_type}: {count}")

        print(f"\nBy namespace:")
        for namespace, count in stats['by_namespace'].items():
            print(f"  {namespace}: {count}")

        if stats['unique_tags'] > 0:
            print(f"\nUnique tags: {stats['unique_tags']}")
            print(f"Tags: {', '.join(stats['tags'])}")

        # Show registry path
        print(f"\nRegistry path: {get_registry_path()}")

        return 0

    except Exception as e:
        print_error(f"Failed to get stats: {e}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for tu CLI."""
    parser = argparse.ArgumentParser(
        prog="tu",
        description="Terminal Utils - unified entry point for scripts and commands",
        add_help=False
    )

    # Global options
    parser.add_argument(
        "--help", "-h",
        action="help",
        help="Show this help message and exit"
    )

    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all registered commands"
    )

    parser.add_argument(
        "--filter",
        metavar="PATTERN",
        help="Filter commands by pattern (with --list)"
    )

    parser.add_argument(
        "--show",
        metavar="NAME",
        dest="show_name",
        help="Show details of a registered command"
    )

    parser.add_argument(
        "--register",
        action="store_true",
        help="Register a new command"
    )

    parser.add_argument(
        "--unregister",
        metavar="NAME",
        dest="unregister_name",
        help="Unregister a command"
    )

    parser.add_argument(
        "--rename",
        nargs=2,
        metavar=("OLD", "NEW"),
        help="Rename a command"
    )

    # Options for --register
    parser.add_argument(
        "--name",
        help="Name for the registered command (with --register)"
    )

    parser.add_argument(
        "--type",
        choices=["shell", "python_module", "python_callable"],
        help="Type of command (with --register)"
    )

    parser.add_argument(
        "--description",
        help="Description of the command (with --register)"
    )

    parser.add_argument(
        "--tags",
        help="Comma-separated tags (with --register)"
    )

    parser.add_argument(
        "--force-dot-name",
        action="store_true",
        help="Allow registering dotted names without confirmation (with --register)"
    )

    # Global execution options
    parser.add_argument(
        "--subshell",
        metavar="DIR",
        help="Run command in a subdirectory"
    )

    # Completion support
    parser.add_argument(
        "--complete",
        metavar="PARTIAL",
        dest="complete_partial",
        help="Complete command names (for shell completion)"
    )

    parser.add_argument(
        "--completion-script",
        metavar="SHELL",
        choices=["bash", "zsh", "fish"],
        help="Print completion script for shell"
    )

    parser.add_argument(
        "--install-completion",
        metavar="SHELL",
        choices=["bash", "zsh", "fish"],
        dest="install_completion_shell",
        help="Show instructions to install completion for shell"
    )

    # Utility commands
    parser.add_argument(
        "--export",
        metavar="PATH",
        dest="export_path",
        help="Export registry to a file"
    )

    parser.add_argument(
        "--import",
        metavar="PATH",
        dest="import_path",
        help="Import registry from a file"
    )

    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge when importing (with --import)"
    )

    parser.add_argument(
        "--validate",
        nargs="?",
        const="",
        metavar="NAME",
        dest="validate_name",
        help="Validate command(s) - all if no name given"
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show registry statistics"
    )

    # Positional arguments for running commands
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to run"
    )

    parser.add_argument(
        "args",
        nargs="*",
        help="Arguments to pass to the command"
    )

    # For --register, we need the target
    parser.add_argument(
        "target",
        nargs="?",
        help="Target for --register"
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for tu CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code.
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle different modes
    if args.list:
        return list_commands_cli(args)

    if args.show_name:
        args.name = args.show_name
        return show_command_cli(args)

    if args.unregister_name:
        args.name = args.unregister_name
        return unregister_command_cli(args)

    if args.rename:
        args.old_name, args.new_name = args.rename
        return rename_command_cli(args)

    if args.complete_partial is not None:
        args.partial = args.complete_partial
        return complete_cli(args)

    if args.completion_script:
        args.shell = args.completion_script
        return completion_script_cli(args)

    if args.install_completion_shell:
        args.shell = args.install_completion_shell
        return install_completion_cli(args)

    if args.export_path:
        return export_registry_cli(args)

    if args.import_path:
        return import_registry_cli(args)

    if args.validate_name is not None:
        return validate_cli(args)

    if args.stats:
        return stats_cli(args)

    if args.register:
        # For --register, the command/target is in different places
        if args.command:
            args.target = args.command
        elif not hasattr(args, "target") or not args.target:
            print_error("--register requires a target")
            return 1
        return register_command_cli(args)

    # If no command specified, default to list
    if not args.command:
        args.filter = None
        return list_commands_cli(args)

    # Otherwise, run the command
    return run_command_cli(args)


if __name__ == "__main__":
    sys.exit(main())
