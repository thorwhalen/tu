# tu Examples

This directory contains examples demonstrating various features of the `tu` package.

## Files

### `basic_usage.py`

Demonstrates basic programmatic usage of tu:
- Registering shell commands
- Listing commands
- Running commands with captured output
- Getting command information
- Unregistering commands

Run with:
```bash
python examples/basic_usage.py
```

### `callable_example.py`

Shows how to create and register Python callable functions:
- Defining functions with the correct signature
- Registering callables
- Executing callables via tu

Run with:
```bash
python examples/callable_example.py
```

Or after running the example, use the CLI:
```bash
tu greet Alice
tu add 10 20 30
```

## CLI Examples

### Register and Run Commands

```bash
# Register a simple shell command
tu --register --name hello --type shell "echo 'Hello, World!'"

# Run it
tu hello

# Register with a description and tags
tu --register --name build --description "Build the project" --tags "build,ci" "make build"

# List all commands
tu --list

# Filter commands
tu --list --filter build
```

### Python Module Examples

```bash
# Register a Python module (type auto-inferred)
tu --register http.server

# Run it (defaults to port 8000)
tu server

# Or run without registration (dotted-name rule)
tu json.tool < data.json
```

### Managing Commands

```bash
# Show command details
tu --show hello

# Rename a command
tu --rename hello greeting

# Unregister a command
tu --unregister greeting
```

### Namespaces

```bash
# Register commands with namespaces
tu --register --name data:import "python import_data.py"
tu --register --name data:export "python export_data.py"
tu --register --name data:clean "python clean_data.py"

# List commands (they'll be grouped by namespace)
tu --list
```

### Global Options

```bash
# Run a command in a subdirectory
tu --subshell ./myproject build
```

### Utility Commands

```bash
# Show registry statistics
tu --stats

# Validate all commands
tu --validate

# Validate a specific command
tu --validate build

# Export registry
tu --export backup.json

# Import registry
tu --import backup.json

# Merge imported registry
tu --import other_commands.json --merge
```

### Shell Completion

```bash
# Get completion script for bash
tu --completion-script bash

# Get installation instructions
tu --install-completion bash

# For zsh
tu --install-completion zsh

# For fish
tu --install-completion fish
```

## Notes

- All examples use temporary registries that are cleaned up after execution
- Some examples may require additional setup or dependencies
- See the main README.md for more comprehensive documentation
