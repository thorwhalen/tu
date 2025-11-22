"""
Basic usage examples for the tu package.

This script demonstrates how to use tu both programmatically and via CLI.
"""

import tu

# Example 1: Register a simple shell command
print("Example 1: Register a shell command")
print("=" * 50)

try:
    cmd = tu.register_command(
        target="echo 'Hello from tu!'",
        name="greet",
        type="shell",
        description="A simple greeting command"
    )
    print(f"Registered: {cmd.name} ({cmd.type})")
except tu.NameCollisionError:
    print("Command 'greet' already exists")

print()

# Example 2: List all registered commands
print("Example 2: List all commands")
print("=" * 50)

commands = tu.list_commands()
for cmd in commands:
    print(f"  {cmd.name}: {cmd.description or '(no description)'}")

print()

# Example 3: Run a command
print("Example 3: Run a command")
print("=" * 50)

result = tu.run("greet", capture_output=True)
print(f"Exit code: {result.returncode}")
print(f"Output: {result.stdout.strip()}")

print()

# Example 4: Register a Python module
print("Example 4: Register a Python module")
print("=" * 50)

try:
    cmd = tu.register_command(
        target="json.tool",
        name="json-format",
        description="Format JSON with json.tool"
    )
    print(f"Registered: {cmd.name} ({cmd.type})")
except tu.NameCollisionError:
    print("Command 'json-format' already exists")

print()

# Example 5: Get command info
print("Example 5: Get command info")
print("=" * 50)

cmd = tu.get_command_info("greet")
if cmd:
    print(f"Name: {cmd.name}")
    print(f"Type: {cmd.type}")
    print(f"Target: {cmd.target}")
    print(f"Created: {cmd.created_at}")
    print(f"Updated: {cmd.updated_at}")

print()

# Clean up examples
print("Cleaning up examples...")
try:
    tu.unregister_command("greet")
    tu.unregister_command("json-format")
    print("Cleanup complete!")
except tu.UnknownCommandError:
    pass
