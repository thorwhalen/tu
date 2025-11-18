# tu - Terminal Utils

**Quick access to your favorite scripts and commands**

`tu` provides a unified entry point for running scripts and commands under a single, hierarchical namespace. Stop remembering dozens of script locations and complex command patterns - register them once with `tu` and invoke them easily.

## Features

- **Single Entry Point**: Run all your scripts and commands via `tu <name> [args...]`
- **Hierarchical Namespaces**: Organize commands with namespaces like `data:export`, `infra:deploy:prod`
- **Multiple Command Types**: Support for shell commands, Python modules, and Python callables
- **Dotted-Name Rule**: Automatically run Python modules without registration (e.g., `tu mypackage.mymodule`)
- **Shell Completion**: Tab completion for bash, zsh, and fish
- **Python API**: Full programmatic access matching CLI capabilities
- **Global Options**: Transform execution with options like `--subshell`
- **Smart Suggestions**: Get helpful suggestions when commands aren't found

## Installation

```bash
pip install tu
```

Or install in development mode:

```bash
git clone https://github.com/thorwhalen/tu.git
cd tu
pip install -e .
```

## Quick Start

### Register a command

```bash
# Register a shell command
tu --register --name clean --description "Clean build artifacts" "make clean"

# Register a Python module (type and name auto-inferred)
tu --register mypackage.deploy

# Register a Python callable
tu --register --name migrate "myapp.db:migrate_database"
```

### List registered commands

```bash
tu --list
```

Output:
```
clean - Clean build artifacts

data:
  export - Export data to CSV
  import - Import data from CSV

infra:
  deploy - Deploy to production
```

### Run a command

```bash
# Run a registered command
tu clean

# Run with arguments
tu data:export --format json --output data.json

# Run a Python module (without registration)
tu mypackage.mymodule --arg value
```

### Manage commands

```bash
# Show command details
tu --show clean

# Rename a command
tu --rename clean cleanup

# Unregister a command
tu --unregister cleanup
```

## Command Types

### Shell Commands

Execute shell commands or scripts:

```bash
# Simple command
tu --register --name ls --type shell "ls -la"

# Script path
tu --register --name deploy --type shell "./scripts/deploy.sh"

# Run it
tu deploy
```

### Python Modules

Execute Python modules using `python -m`:

```bash
# Register (type auto-inferred from dotted name)
tu --register myapp.server

# Run
tu server  # Runs: python -m myapp.server
```

### Python Callables

Execute Python functions directly:

```bash
# Register a function
tu --register --name backup "myapp.tasks:backup_database"

# The function signature should be:
# def backup_database(args: list[str]) -> int | None:
#     # args contains command-line arguments
#     return 0  # exit code
```

Example function:

```python
# myapp/tasks.py
def backup_database(args: list[str]) -> int:
    """Backup the database.

    Args:
        args: Command-line arguments passed to the function

    Returns:
        Exit code (0 for success)
    """
    if "--help" in args:
        print("Usage: tu backup [--output PATH]")
        return 0

    # Backup logic here
    print("Database backed up successfully!")
    return 0
```

## Dotted-Name Rule

If you try to run a command that isn't registered but contains a dot (`.`), `tu` automatically interprets it as a Python module:

```bash
# Not registered, but will work
tu json.tool < data.json

# Equivalent to
python -m json.tool < data.json
```

This provides seamless Python module execution without explicit registration.

## Namespaces

Use colons (`:`) to create hierarchical namespaces:

```bash
tu --register --name data:export "python -m myapp.export"
tu --register --name data:import "python -m myapp.import"
tu --register --name infra:deploy:staging "./deploy.sh staging"
tu --register --name infra:deploy:prod "./deploy.sh prod"
```

List commands by namespace:

```bash
tu --list --filter data
```

## Global Options

### --subshell

Run a command in a specific directory:

```bash
tu --subshell /path/to/project build
```

This is equivalent to:

```bash
(cd /path/to/project && tu build)
```

## Shell Completion

Enable tab completion for your shell:

### Bash

```bash
tu --install-completion bash
```

Add to your `~/.bashrc`:

```bash
eval "$(tu --completion-script bash)"
```

### Zsh

```bash
tu --install-completion zsh
```

Save the completion script:

```bash
tu --completion-script zsh > ~/.zsh/completion/_tu
```

Add to your `~/.zshrc`:

```bash
fpath=(~/.zsh/completion $fpath)
autoload -Uz compinit && compinit
```

### Fish

```bash
tu --completion-script fish > ~/.config/fish/completions/tu.fish
```

## Python API

Use `tu` programmatically in your Python code:

```python
import tu

# List all commands
commands = tu.list_commands()
for cmd in commands:
    print(f"{cmd.name}: {cmd.description}")

# Register a command
tu.register_command(
    target="myapp.deploy",
    name="deploy",
    description="Deploy the application",
    tags=["deployment", "production"]
)

# Get command info
cmd = tu.get_command_info("deploy")
print(f"Command type: {cmd.type}")
print(f"Created: {cmd.created_at}")

# Run a command
result = tu.run("deploy", args=["--env", "prod"])
print(f"Exit code: {result.returncode}")

# Run with captured output
result = tu.run("deploy", args=["--dry-run"], capture_output=True)
print(f"Output: {result.stdout}")

# Rename a command
tu.rename_command("deploy", "deploy-app")

# Unregister a command
tu.unregister_command("deploy-app")
```

## Registry

Commands are stored in a JSON registry at `~/.config/tu/registered_scripts.json`.

You can override this location with the `IC_REGISTERED_SCRIPTS_JSON_FILE` environment variable:

```bash
export IC_REGISTERED_SCRIPTS_JSON_FILE=/custom/path/registry.json
```

### Registry Format

```json
{
  "version": 1,
  "commands": {
    "clean": {
      "type": "shell",
      "target": "make clean",
      "description": "Clean build artifacts",
      "tags": ["build", "cleanup"],
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    },
    "data:export": {
      "type": "python_module",
      "target": "myapp.export",
      "description": "Export data",
      "tags": ["data"],
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    }
  }
}
```

## Advanced Usage

### Tags

Organize commands with tags:

```bash
tu --register --name test --tags "testing,ci" "pytest"
tu --register --name lint --tags "testing,quality" "ruff check"
```

### Command Inference

When registering, `tu` can infer the command type and name:

```bash
# Infers: type=python_module, name=mymodule
tu --register mypackage.mymodule

# Infers: type=python_callable, name=main
tu --register mypackage:main

# Infers: type=shell, name=deploy
tu --register ./scripts/deploy.sh

# Infers: type=shell, name=ls
tu --register ls
```

### Preventing Overwrites

`tu` never silently overwrites commands. If you try to register a name that already exists, you'll get a helpful error:

```bash
$ tu --register --name test "echo new"
Error: Command 'test' already exists.
Use 'tu --unregister test' to remove it,
or 'tu --rename test <new_name>' to rename it.
```

## Examples

### Development Workflow

```bash
# Register common development commands
tu --register --name test "pytest tests/"
tu --register --name lint "ruff check ."
tu --register --name format "ruff format ."
tu --register --name build "python -m build"

# Use them
tu test
tu lint
tu format
tu build
```

### Data Pipeline

```bash
# Register data processing steps
tu --register --name data:fetch "python -m myapp.fetch"
tu --register --name data:process "python -m myapp.process"
tu --register --name data:analyze "python -m myapp.analyze"

# Run the pipeline
tu data:fetch
tu data:process
tu data:analyze
```

### Deployment

```bash
# Register deployment commands
tu --register --name deploy:staging "./deploy.sh staging"
tu --register --name deploy:prod "./deploy.sh prod"

# Deploy
tu deploy:staging
tu deploy:prod
```

## Philosophy

`tu` follows an **interface-to-interface** approach:

- **Small core**: Minimal, composable functionality
- **Thin router**: Pass arguments unchanged, propagate exit codes
- **No discovery**: Only knows about explicitly registered commands (plus dotted-name rule)
- **No overwrites**: Explicit operations prevent accidental data loss
- **Extensible**: Easy to add new command types and global options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

Thor Whalen

## Links

- **GitHub**: https://github.com/thorwhalen/tu
- **Documentation**: Coming soon
- **Issues**: https://github.com/thorwhalen/tu/issues
