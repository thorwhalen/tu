"""Interactive REPL mode for tu."""

import sys
from typing import Optional

from . import api
from .exceptions import TuError


def print_welcome():
    """Print welcome message."""
    print("=" * 60)
    print("  tu - Terminal Utils Interactive Mode")
    print("=" * 60)
    print("Type 'help' for available commands, 'exit' or 'quit' to leave")
    print()


def print_help():
    """Print help message."""
    print("\nAvailable commands:")
    print("  list [PATTERN]      - List registered commands")
    print("  show NAME           - Show command details")
    print("  run NAME [ARGS...]  - Run a command")
    print("  register TARGET     - Register a new command")
    print("  unregister NAME     - Remove a command")
    print("  rename OLD NEW      - Rename a command")
    print("  history [NAME]      - Show command history")
    print("  stats               - Show registry statistics")
    print("  validate [NAME]     - Validate command(s)")
    print("  help                - Show this help")
    print("  exit, quit          - Exit interactive mode")
    print()


def handle_list(args: list[str]) -> None:
    """Handle list command."""
    pattern = args[0] if args else None
    commands = api.list_commands(pattern=pattern)

    if not commands:
        if pattern:
            print(f"No commands matching '{pattern}' found.")
        else:
            print("No commands registered.")
        return

    # Group by namespace
    grouped: dict[str, list] = {}
    for cmd in commands:
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


def handle_show(args: list[str]) -> None:
    """Handle show command."""
    if not args:
        print("Error: show requires a command name")
        return

    cmd = api.get_command_info(args[0])
    if cmd is None:
        print(f"Error: Command '{args[0]}' not found.")
        return

    print(f"\nName: {cmd.name}")
    print(f"Type: {cmd.type}")
    print(f"Target: {cmd.target}")
    if cmd.description:
        print(f"Description: {cmd.description}")
    if cmd.tags:
        print(f"Tags: {', '.join(cmd.tags)}")
    if cmd.aliases:
        print(f"Aliases: {', '.join(cmd.aliases)}")
    if cmd.depends_on:
        print(f"Depends on: {', '.join(cmd.depends_on)}")
    if cmd.env:
        print(f"Environment: {cmd.env}")
    if cmd.timeout:
        print(f"Timeout: {cmd.timeout}s")
    print(f"Created: {cmd.created_at.isoformat()}")
    print(f"Updated: {cmd.updated_at.isoformat()}")
    print()


def handle_run(args: list[str]) -> None:
    """Handle run command."""
    if not args:
        print("Error: run requires a command name")
        return

    name = args[0]
    cmd_args = args[1:]

    try:
        result = api.run(name, args=cmd_args)
        print(f"\n[Exit code: {result.returncode}]")
        if result.duration:
            print(f"[Duration: {result.duration:.2f}s]")
    except TuError as e:
        print(f"Error: {e}")


def handle_register(args: list[str]) -> None:
    """Handle register command."""
    if not args:
        print("Error: register requires a target")
        return

    try:
        cmd = api.register_command(target=args[0])
        print(f"Registered: {cmd.name} ({cmd.type})")
    except TuError as e:
        print(f"Error: {e}")


def handle_unregister(args: list[str]) -> None:
    """Handle unregister command."""
    if not args:
        print("Error: unregister requires a command name")
        return

    try:
        api.unregister_command(args[0])
        print(f"Unregistered: {args[0]}")
    except TuError as e:
        print(f"Error: {e}")


def handle_rename(args: list[str]) -> None:
    """Handle rename command."""
    if len(args) < 2:
        print("Error: rename requires old and new names")
        return

    try:
        api.rename_command(args[0], args[1])
        print(f"Renamed: {args[0]} -> {args[1]}")
    except TuError as e:
        print(f"Error: {e}")


def handle_history(args: list[str]) -> None:
    """Handle history command."""
    from .history import get_command_history, load_history

    if args:
        # Show history for specific command
        entries = get_command_history(args[0], limit=20)
        if not entries:
            print(f"No history found for '{args[0]}'")
            return

        print(f"\nHistory for '{args[0]}':")
    else:
        # Show all history
        entries = load_history(limit=20)
        if not entries:
            print("No history found")
            return

        print("\nRecent command history:")

    for entry in entries:
        args_str = " ".join(entry.args) if entry.args else ""
        print(f"  {entry.executed_at.strftime('%Y-%m-%d %H:%M:%S')} - "
              f"{entry.command_name} {args_str} "
              f"(exit={entry.returncode}, {entry.duration:.2f}s)")


def handle_stats(args: list[str]) -> None:
    """Handle stats command."""
    from .utils import get_registry_stats
    from .registry import get_registry_path

    stats = get_registry_stats()

    print(f"\nTotal commands: {stats['total_commands']}")
    print(f"\nBy type:")
    for cmd_type, count in stats['by_type'].items():
        print(f"  {cmd_type}: {count}")

    print(f"\nBy namespace:")
    for namespace, count in stats['by_namespace'].items():
        print(f"  {namespace}: {count}")

    if stats['unique_tags'] > 0:
        print(f"\nUnique tags: {stats['unique_tags']}")
        print(f"Tags: {', '.join(stats['tags'])}")

    print(f"\nRegistry path: {get_registry_path()}")
    print()


def handle_validate(args: list[str]) -> None:
    """Handle validate command."""
    from .utils import validate_all_commands, validate_command
    from .registry import get_command

    if args:
        # Validate specific command
        cmd = get_command(args[0])
        if cmd is None:
            print(f"Error: Command '{args[0]}' not found.")
            return

        is_valid, error = validate_command(cmd)
        if is_valid:
            print(f"Command '{args[0]}' is valid.")
        else:
            print(f"Command '{args[0]}' is invalid: {error}")
    else:
        # Validate all commands
        results = validate_all_commands()
        invalid = {name: error for name, error in results.items() if error is not None}

        if not invalid:
            print("All commands are valid.")
        else:
            print("Invalid commands found:")
            for name, error in invalid.items():
                print(f"  {name}: {error}")


def repl() -> int:
    """Run the interactive REPL.

    Returns:
        Exit code.
    """
    print_welcome()

    while True:
        try:
            # Read input
            try:
                line = input("tu> ").strip()
            except EOFError:
                print("\nExiting...")
                return 0

            if not line:
                continue

            # Parse command
            parts = line.split()
            command = parts[0].lower()
            args = parts[1:]

            # Handle commands
            if command in ("exit", "quit"):
                print("Exiting...")
                return 0

            elif command == "help":
                print_help()

            elif command == "list":
                handle_list(args)

            elif command == "show":
                handle_show(args)

            elif command == "run":
                handle_run(args)

            elif command == "register":
                handle_register(args)

            elif command == "unregister":
                handle_unregister(args)

            elif command == "rename":
                handle_rename(args)

            elif command == "history":
                handle_history(args)

            elif command == "stats":
                handle_stats(args)

            elif command == "validate":
                handle_validate(args)

            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\n(Use 'exit' or 'quit' to leave)")
            continue

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    return 0
