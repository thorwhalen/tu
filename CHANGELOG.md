# Changelog

All notable changes to the tu project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2025-11-18

### Added

#### Core Features
- **Registry System**: JSON-based command registry at `~/.config/tu/registered_scripts.json`
  - Support for environment variable override via `IC_REGISTERED_SCRIPTS_JSON_FILE`
  - Atomic writes with proper error handling
  - Versioned schema for future extensibility

- **Command Types**: Support for three command types
  - `shell`: Execute shell commands and scripts
  - `python_module`: Execute Python modules via `python -m`
  - `python_callable`: Execute Python functions directly

- **CLI Interface**: Comprehensive command-line interface
  - `tu <command> [args...]` - Run registered commands
  - `--register` - Register new commands with auto-inference
  - `--unregister` - Remove commands
  - `--rename` - Rename commands
  - `--list` - List all commands with namespace grouping
  - `--show` - Show detailed command information
  - `--help` - Display help

- **Dotted-Name Rule**: Automatic Python module execution
  - Unregistered dotted names (e.g., `tu json.tool`) execute as `python -m json.tool`
  - Registered commands take precedence

- **Hierarchical Namespaces**: Organize commands with colon-separated namespaces
  - Example: `data:export`, `infra:deploy:prod`
  - Automatic grouping in list views

- **Python API**: Full programmatic access
  - `tu.list_commands()` - List registered commands
  - `tu.get_command_info()` - Get command details
  - `tu.register_command()` - Register commands
  - `tu.unregister_command()` - Remove commands
  - `tu.rename_command()` - Rename commands
  - `tu.run()` - Execute commands with optional output capture

#### Advanced Features

- **Global Options Framework**: Extensible command transformations
  - `--subshell <dir>` - Run commands in specific directories

- **Shell Completion**: Tab completion support
  - Bash completion script
  - Zsh completion script
  - Fish completion script
  - `--install-completion` for setup instructions
  - `--completion-script` to generate scripts

- **Smart Suggestions**: Fuzzy command name matching
  - Levenshtein distance-based suggestions for unknown commands

- **Command Validation**: Verify command targets exist
  - `--validate` - Validate all commands
  - `--validate <name>` - Validate specific command
  - Checks for file existence, PATH availability, and Python module imports

- **Registry Management**:
  - `--export <path>` - Export registry to file
  - `--import <path>` - Import registry from file
  - `--import <path> --merge` - Merge imported commands
  - `--stats` - Show registry statistics

#### Safety Features

- **No Silent Overwrites**: Commands must be explicitly removed or renamed
  - Clear error messages with remediation instructions
  - Protection against accidental data loss

- **Name Validation**: Strict naming rules
  - Allowed characters: alphanumeric, underscore, dash, dot, colon
  - Prevention of double colons, leading/trailing colons

- **Dotted Name Warnings**: Interactive confirmation for registering dotted names
  - Prevents conflicts with the dotted-name rule

#### Developer Features

- **Comprehensive Test Suite**: 51 tests with 100% pass rate
  - Unit tests for all core modules
  - Integration tests for CLI
  - Fixtures for isolated testing

- **Type Annotations**: Full type hints throughout the codebase
  - Better IDE support
  - Improved code quality

- **Documentation**:
  - Comprehensive README with examples
  - Docstrings for all public APIs
  - Example scripts demonstrating usage
  - CLI help messages

#### Data Models

- `RegisteredCommand`: Dataclass for command metadata
  - Name, type, target, description, tags
  - Created/updated timestamps

- `RunResult`: Command execution results
  - Return code, stdout, stderr

- `ExecutionPlan`: Command execution context
  - Command type, target, args, cwd, env

### Dependencies

- Python 3.10+ required
- No external dependencies for core functionality
- Optional dev dependencies: pytest, ruff

### Notes

This is the initial release implementing Phase 1 (MVP) and Phase 2 features from the specification, plus additional utility features.

Future releases will include:
- Help store and search (Phase 3)
- Argument-level completion
- Project-local registries
- Additional global options
