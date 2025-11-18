"""
Example of using Python callables with tu.

This demonstrates how to create and register functions that can be
executed via tu.
"""


def greet(args: list[str]) -> int:
    """A simple greeting function.

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success)
    """
    if "--help" in args:
        print("Usage: tu greet [NAME]")
        print("Greet someone by name")
        return 0

    name = args[0] if args else "World"
    print(f"Hello, {name}!")
    return 0


def add_numbers(args: list[str]) -> int:
    """Add numbers from command-line arguments.

    Args:
        args: List of numbers to add

    Returns:
        Exit code (0 for success, 1 for error)
    """
    if "--help" in args or not args:
        print("Usage: tu add NUMBER1 NUMBER2 ...")
        print("Add numbers together")
        return 0 if "--help" in args else 1

    try:
        numbers = [float(arg) for arg in args]
        result = sum(numbers)
        print(f"Sum: {result}")
        return 0
    except ValueError:
        print("Error: All arguments must be numbers")
        return 1


def main():
    """Demonstrate registering and using callables."""
    import tu

    print("Registering callable functions")
    print("=" * 50)

    # Register the greet function
    try:
        tu.register_command(
            target="examples.callable_example:greet",
            name="greet",
            description="Greet someone"
        )
        print("Registered: greet")
    except tu.NameCollisionError:
        print("greet already registered")

    # Register the add_numbers function
    try:
        tu.register_command(
            target="examples.callable_example:add_numbers",
            name="add",
            description="Add numbers together"
        )
        print("Registered: add")
    except tu.NameCollisionError:
        print("add already registered")

    print()

    # Test the functions
    print("Testing greet function")
    print("=" * 50)
    result = tu.run("greet", args=["Alice"])
    print(f"Exit code: {result.returncode}")

    print()

    print("Testing add function")
    print("=" * 50)
    result = tu.run("add", args=["10", "20", "30"])
    print(f"Exit code: {result.returncode}")

    print()

    # Cleanup
    print("Cleaning up...")
    try:
        tu.unregister_command("greet")
        tu.unregister_command("add")
        print("Done!")
    except tu.UnknownCommandError:
        pass


if __name__ == "__main__":
    main()
