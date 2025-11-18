
Specification: tu (“Terminal Utils”) – Script Registration and Routing Package
	1.	Purpose and scope

⸻

The tu project provides a single, extensible entry point for running many scripts and commands under one unified, namespaced namespace.

The core goals:
	•	Allow users (primarily Python developers) to:
	•	Register scripts and commands under hierarchical names such as my_script or my:nested:script.
	•	Invoke them via a single CLI entry point: tu my_script ... or tu my:nested:script ....
	•	Treat tu-registered commands as if they were “normal” scripts with shell completion.
	•	Provide a thin routing layer that:
	•	Resolves a registered name to an executable target.
	•	Forwards arguments unchanged.
	•	Propagates exit codes.
	•	Provide a Python API that mirrors the CLI’s capabilities (registration, listing, execution).
	•	Evolve toward richer capabilities (global options as composable patterns, persisted help strings, search) without breaking the simple mental model.

Discovery is explicitly out of scope: tu only knows about commands that are explicitly registered, except for a special built-in rule for dotted names (Python modules) described later.

The design follows an interface-to-interface approach: the CLI, shell, and Python APIs on one side; the registered commands (scripts, Python modules, executables) on the other. tu is the small, composable layer that translates between these interfaces.
	2.	Core concepts and terminology

⸻

Registered command
	•	A named entry in the registry, identified by a fully qualified name (FQN).
	•	Each registered command has:
	•	A fully qualified name (e.g. clean, data:export, deploy:prod).
	•	A target that describes what to actually run (shell command, Python module, Python callable, etc.).
	•	A type that clarifies how to execute the target.
	•	Optional metadata (description, tags, timestamps), designed to be easily extended.

Fully qualified name (FQN)
	•	Textual identifier used on the CLI: tu <name> [args...].
	•	Namespaces are separated with ::
	•	Examples: clean, data:export, infra:deploy:prod.
	•	Constraints:
	•	Allowed characters per segment (recommendation for implementation): [a-zA-Z0-9_.-]+ with the understanding that . carries special semantics (see dotted names).
	•	Entire FQN as used on the CLI may be something like my:namespace:script, where my, namespace, script are segments.
	•	Collisions:
	•	FQNs are unique in the registry.
	•	Attempting to register an already existing FQN must fail with a clear message:
	•	No overwrites.
	•	The user is told to remove or rename the existing entry first, using provided tools.

Dotted name rule (Python modules)
	•	If a command name used on the CLI (the first token after tu) contains a dot (.) and is not found in the registry, tu interprets it as a Python module and executes:
	•	python -m <dotted_name> [args...]
	•	This is a built-in routing rule for Python users: tu mypkg.mymodule arg1 arg2 behaves like calling python -m mypkg.mymodule arg1 arg2.
	•	If the user attempts to register a name that contains a dot:
	•	The tool must warn that dotted names have special meaning and ask for explicit confirmation to proceed.
	•	Once registered, the registered command takes precedence over the dotted-name default behavior.

Command types (initial set)
	•	shell: target is a shell command or path (e.g. ls, /usr/bin/ffmpeg, ./scripts/deploy.sh).
	•	python_module: target is a module path (e.g. mypkg.mymodule).
	•	python_callable (Phase 1 support in the registry and API; may not need a dedicated CLI shorthand immediately):
	•	Target is module:function or package.module:function.
	•	The implementation uses importlib to load and call the function.
	•	The callable receives arguments in a defined way (e.g. list of strings, or an argparse-like interface; see section 7).

These types can be extended in later phases (e.g. containerized commands, scripts with specific interpreters).

Registry
	•	The persistent JSON configuration file storing registered commands.
	•	Default location:
	•	~/.config/tu/registered_scripts.json
	•	Override via environment variable:
	•	IC_REGISTERED_SCRIPTS_JSON_FILE
	•	If set, this path is used instead of the default.
	•	Registry is the canonical source of truth for registered commands.

Help store (Phase 3)
	•	A file-based store of help text per FQN, used mainly for search and tooling.
	•	Default location:
	•	~/.local/share/tu/help_strings/{fully_qualified_name}.txt
	•	May be overridable via an environment variable (e.g. IC_HELP_STRINGS_DIR) at design time.

	3.	High-level behavior

⸻

	•	tu acts as a thin, predictable router:
	•	Parses global options.
	•	Determines the command name and arguments.
	•	Resolves the command name to a registered command or a dotted-name Python module (if applicable).
	•	Executes the underlying command (shell, python -m, Python callable).
	•	Returns the underlying command’s exit code.
	•	No automatic discovery:
	•	If a name is not registered and does not contain a dot, tu fails with a clear “unknown command” error.
	•	If a name contains a dot and is not registered, the dotted-name rule applies.
	•	Namespaces are purely textual:
	•	my:nested:script is namespaced naming; tu does not impose special semantics beyond name resolution and listing/grouping.
	•	Collisions are prohibited:
	•	The system never silently overwrites registered entries.

	4.	CLI interface

⸻

4.1 Top-level CLI usage

The tu package installs a console script entry point:
	•	Executable name: tu
	•	Entry point in packaging: tu = tu.cli:main

Basic usages (Phase 1):
	•	List commands:
	•	tu
	•	tu --list
	•	Run a command:
	•	tu <name> [args...]
	•	Manage registry:
	•	tu --register [options] <target>
	•	tu --unregister <name>
	•	tu --rename <old_name> <new_name>
	•	tu --show <name>

Global options (initial set):
	•	--list / -l
List all registered commands (organized by namespace when appropriate).
	•	--register
Create a new registry entry (see below).
	•	--unregister
Remove a registry entry by FQN.
	•	--rename
Rename a registry entry.
	•	--show
Show details of a registered command.
	•	--help / -h
Show general help.
	•	Phase 2: additional global options such as --subshell (see section 10).

Parsing rules:
	•	All tokens starting with - before the first non-option token are treated as global options.
	•	The first non-option token (if present) is treated as the command name (FQN or dotted name) when --register, --unregister, etc. are not used.
	•	If both “management” flags and a command name are present in a conflicting way, the CLI should fail with a clear error.

4.2 Running commands

Syntax
	•	tu <name> [args...]

Behavior:
	1.	Determine <name> as the first non-option token.
	2.	Try to resolve <name> as a fully qualified name in the registry.
	3.	If found:
	•	Execute according to its type.
	4.	If not found and <name> contains a dot:
	•	Execute python -m <name> [args...].
	5.	Otherwise:
	•	Print “Unknown command” with suggestions (e.g. closest matches) and exit with a non-zero code.

Examples:
	•	Registered command clean → tu clean.
	•	Registered command data:export → tu data:export --format csv.
	•	Unregistered command mypkg.mymodule → tu mypkg.mymodule behaves as python -m mypkg.mymodule.

4.3 Registering commands

Syntax (Phase 1)
	•	tu --register [--name <fqn>] [--type <type>] <target>

Semantics:
	•	<target> is required.
	•	--type:
	•	Allowed values: shell, python_module, python_callable.
	•	If omitted, tu infers the type from <target>:
	•	If <target> looks like module:function (contains : and no spaces), default to python_callable.
	•	Else if <target> looks like a Python module path (contains . and no spaces, and is importable), default to python_module.
	•	Otherwise, default to shell.
	•	Inference should be implemented as a small, explicit chain with graceful fallback to shell to avoid false assumptions.
	•	--name:
	•	If provided, use this as the FQN (subject to name validation).
	•	If omitted, a default name is derived from <target>:
	•	For python_module: use the last path segment (e.g. mypkg.mymodule → mymodule).
	•	For python_callable: use the function name (e.g. mypkg.mymodule:main → main).
	•	For shell:
	•	If target is a path, use the basename (e.g. /usr/local/bin/deploy → deploy).
	•	If target is a simple command word, use that word (e.g. ffmpeg → ffmpeg).
	•	Default name is always at the first level (no : unless explicitly provided by the user via --name).
	•	Name collisions:
	•	If the derived or provided FQN already exists in the registry:
	•	Registration fails.
	•	The error message explains:
	•	That overwriting is not allowed.
	•	How to:
	•	tu --unregister <name> to delete the existing entry.
	•	tu --rename <old_name> <new_name> to free the name.
	•	Or re-run registration with a different --name.
	•	Dotted names:
	•	If --name or derived name contains a dot:
	•	tu must print a warning that this name conflicts with the dotted-name rule.
	•	The CLI should require explicit confirmation (e.g. --force-dot-name flag or interactive y/n depending on mode) to proceed.

Example:
	•	tu --register mypkg.mymodule
	•	Type inferred as python_module.
	•	Default name: mymodule.
	•	If mymodule is free, registry gets an entry: { "name": "mymodule", "type": "python_module", "target": "mypkg.mymodule" }.

4.4 Unregistering and renaming commands

Unregister
	•	tu --unregister <name>
	•	Removes a registry entry.
	•	If <name> does not exist:
	•	Print an informative warning and exit with non-zero code (but this is a soft failure, not a crash).

Rename
	•	tu --rename <old_name> <new_name>
	•	Renames an existing registry entry’s FQN.
	•	Preconditions:
	•	old_name must exist.
	•	new_name must not exist.
	•	If new_name exists, renaming fails with a collision message and instructions (same anti-overwrite rule).

4.5 Listing and showing commands

List
	•	tu (no arguments) or tu --list
	•	Behavior:
	•	List all registered commands, grouped by top-level namespace.
	•	If namespaces are present, display something like:
	•	data:export – description
	•	data:import – description
	•	infra:deploy – description
	•	clean – description
	•	Optional flags (Phase 1 or 2):
	•	--filter <pattern>: filter by substring match in name.
	•	--type <type>: filter by command type.

Show
	•	tu --show <name>
	•	Print detailed JSON-like information about the command:
	•	FQN, type, target, creation time, last updated time, and any metadata.

	5.	Registry format

⸻

The registry is a JSON file at ~/.config/tu/registered_scripts.json or IC_REGISTERED_SCRIPTS_JSON_FILE.

Recommended schema (versioned):

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
      "target": "mypkg.export",
      "description": "Export data",
      "tags": ["data"],
      "created_at": "...",
      "updated_at": "..."
    }
  }
}

Implementation guidelines:
	•	Always read-modify-write with care:
	•	Use file locking or atomic write (write to temp file then rename) to avoid corruption.
	•	Validate JSON structure:
	•	If file is missing: treat as an empty registry.
	•	If file is invalid: fail with a clear message and suggestion to back up and reconstruct.
	•	The schema must be easy to extend:
	•	Additional fields (e.g. help_captured, env, working_directory) should be optional and backward-compatible.

	6.	Python API

⸻

The Python API mirrors the CLI behavior and exposes a small set of composable functions. The main module is tu.

6.1 Core functions
	•	tu.list_commands(pattern: str | None = None) -> list[RegisteredCommand]
	•	tu.get_command(name: str) -> RegisteredCommand | None
	•	tu.register_command(target: str, *, name: str | None = None, type: str | None = None, description: str | None = None, tags: list[str] | None = None, allow_dot_name: bool = False) -> RegisteredCommand
	•	tu.unregister_command(name: str) -> None
	•	tu.rename_command(old_name: str, new_name: str) -> None
	•	tu.run(name: str, args: list[str] | None = None, *, capture_output: bool = False) -> RunResult
	•	RunResult may include:
	•	returncode: int
	•	stdout: str | None
	•	stderr: str | None

6.2 Data structures
	•	RegisteredCommand (likely a dataclass):
	•	name: str (FQN)
	•	type: Literal["shell", "python_module", "python_callable", ...]
	•	target: str
	•	description: str | None
	•	tags: list[str]
	•	created_at: datetime
	•	updated_at: datetime
	•	RunResult:
	•	returncode: int
	•	stdout: str | None
	•	stderr: str | None

6.3 Semantics
	•	Python API should share the same resolution rules as the CLI:
	•	tu.run("mypkg.mymodule", args) should use the same dotted-name rule and registry as tu mypkg.mymodule.
	•	The API should be designed in a functional style as much as reasonable:
	•	Pure functions over an explicit registry object can be exposed (e.g. load_registry(path), save_registry(registry, path)), enabling alternative configurations.
	•	Error handling:
	•	Use specific exception types (UnknownCommandError, NameCollisionError, RegistryCorruptedError, etc.) rather than generic exceptions.

	7.	Execution semantics

⸻

7.1 General rules
	•	tu is a thin router:
	•	The underlying command’s behavior is not interpreted.
	•	Arguments after <name> are passed as-is to the underlying command.
	•	Working directory:
	•	Commands run in the current process working directory by default.
	•	Phase 2 global options (e.g. --subshell) can alter this behavior.

7.2 Running shell commands
	•	For shell type:
	•	Use subprocess with:
	•	shell=True if the target is treated as a shell command.
	•	Or shell=False and split the target into argv if the command is a path plus arguments. This must be specified explicitly in the implementation.
	•	Propagate exit code unchanged.
	•	Arguments passed via tu:
	•	If target is a pre-defined command, args passed to tu are appended to that command’s arguments.

7.3 Running Python modules
	•	For python_module type:
	•	Execute the module as python -m <module> [args...].
	•	For dotted-name rule (unregistered):
	•	Equivalent behavior: python -m <name> [args...].

Implementation detail:
	•	Use runpy or subprocess depending on isolation needs.
	•	For a thin router, subprocess is simpler and behaviorally closer to actual python -m in the user’s environment.

7.4 Running Python callables
	•	For python_callable type:
	•	Target string: module:function.
	•	Resolver:
	•	Import the module via importlib.import_module.
	•	Retrieve the attribute function from the module.
	•	Call signature:
	•	Initial implementation: callable(args: list[str]):
	•	The function must accept a single argument: a list of strings.
	•	It returns an integer exit code or None (interpreted as 0).
	•	This is simple and matches the “thin router” philosophy; richer signatures can come later.
	•	Exit code:
	•	If the function returns an integer, use that as exit code.
	•	If it returns None, treat as 0.
	•	If it raises an exception, propagate a non-zero exit code and print stack trace.

	8.	Shell completion and autosuggest

⸻

Goal: completions for command names as if they were normal scripts.

8.1 Scope
	•	Support at least bash and zsh (Phase 1); fish can be Phase 2.
	•	Provide name-level completion:
	•	When user types tu <TAB>, they see registered command names and any dotted-name suggestions (optional).
	•	Argument-level completion is aspirational (Phase 3 and help-based).

8.2 Mechanism
	•	tu must be able to output a completion script:
	•	tu --install-completion bash
	•	tu --install-completion zsh
	•	The completion scripts:
	•	Hook into shell completion.
	•	Call back into tu (e.g. tu --complete <partial>) to get a list of candidate names.
	•	tu --complete <partial>:
	•	Internal, not meant for human use.
	•	Return a newline-separated list of candidate FQNs starting with <partial>.

8.3 Fuzzy suggestions
	•	When a user tries to run tu cleam and clean exists:
	•	tu should suggest possible matches (Levenshtein-based or similar).
	•	This is not full fuzzy-execution (no automatic “did you mean; press Y to run”), but at least diagnostics.

	9.	Help strings and search (Phase 3)

⸻

Phase 3 introduces a help store for each registered command.

9.1 Help storage
	•	Default directory:
	•	~/.local/share/tu/help_strings/
	•	File per FQN:
	•	Path: ~/.local/share/tu/help_strings/{fqn}.txt
	•	Use FQN as filename (with safe character mapping if necessary).

9.2 Capturing help

Possible CLI interactions (Phase 3, for specification):
	•	tu --capture-help <name> [--command-help-flag <flag>]
	•	Runs the underlying command with its help flag (default --help).
	•	Captures stdout and stores it in the help store file.
	•	Alternatively, allow manual editing:
	•	tu --edit-help <name> which opens the file in $EDITOR.

9.3 Help search
	•	tu --search-help <pattern>:
	•	Search across all help text files for pattern.
	•	Return matching commands with context.
	•	Future integration:
	•	Argument-level completion based on static parsing or heuristics over help text.

	10.	Global options and patterns (Phase 2)

⸻

Phase 2 introduces global options that map common shell patterns to reusable transformations of the underlying command execution.

Example: --subshell.

10.1 --subshell option
	•	Syntax:
	•	tu --subshell <folder> <name> [args...]
	•	Semantics:
	•	Equivalent to running:
	•	(cd <folder> && tu <name> [args...])
	•	In implementation, avoid actually invoking tu recursively; instead:
	•	Change directory for the subprocess only.
	•	Registration:
	•	subshell is a default, built-in global option.
	•	The framework should allow adding more such options later via code.

10.2 Global options framework
	•	A global option is a mapping:
	•	option_name -> transformation
	•	Transformation:
	•	A function that takes an ExecutionPlan (command and arguments) and returns a new ExecutionPlan.
	•	Example ExecutionPlan structure:
	•	command_type
	•	target
	•	cwd
	•	env
	•	argv
	•	Global options can be composed:
	•	tu --subshell src --some-future-option ... <name> [args...] applies transformations in sequence.
	•	Implementation guidance:
	•	Maintain a registry of global options in Python:
	•	GLOBAL_OPTIONS: dict[str, Callable[[ExecutionPlan, list[str]], ExecutionPlan]].
	•	This registry allows future extension and potentially user-defined global options.

	11.	Internal architecture guidelines

⸻

Architecture should reflect the i2i philosophy: small core, composable, loosely coupled layers, interfaces all the way down.

11.1 Suggested module structure
	•	tu.cli
	•	Argument parsing, top-level command dispatch.
	•	tu.registry
	•	Load/save registry JSON.
	•	CRUD operations on RegisteredCommand.
	•	tu.resolve
	•	Resolution logic:
	•	Registry lookup.
	•	Dotted-name rule.
	•	tu.execute
	•	Execution of ExecutionPlan.
	•	Shell, Python module, Python callable execution.
	•	tu.options
	•	Global options framework (--subshell, future options).
	•	tu.completion
	•	Completion script generation.
	•	Completion backend (--complete).
	•	tu.help_store (Phase 3)
	•	Help capture, storage, search.

11.2 Design principles
	•	Keep core logic pure where practical:
	•	Registry operations as pure transformations over in-memory structures.
	•	I/O operations (file read/write, subprocess) at well-defined boundaries.
	•	Introduce a small internal “command DSL”:
	•	Commands represented as ExecutionPlan objects.
	•	Global options and other transformations are functions ExecutionPlan -> ExecutionPlan.
	•	Avoid hidden global state:
	•	Functions that operate on the registry should accept a registry object and/or path explicitly, with convenience wrappers for “default registry”.
	•	Align with “idea-to-implementation”:
	•	The registry and CLI interface should be easy to manipulate programmatically, allowing incremental building of tooling on top of tu.
	•	Aim for extensibility without complexity:
	•	Use simple data structures (dataclasses, dicts).
	•	Version the registry schema from the beginning.
	•	Keep types small and orthogonal.

11.3 Testing and ergonomics
	•	Provide unit tests for:
	•	Registry operations.
	•	Name resolution (including collision handling and dotted-name logic).
	•	Execution behaviors for each command type.
	•	Provide integration tests for:
	•	CLI scenarios (via subprocess or click/typer testing utilities if used).
	•	Consider using a mainstream CLI library (e.g. argparse, click, typer) but not in a way that locks the design into a monolith:
	•	Parsing and routing logic should remain conceptually simple and open to refactoring.

	12.	Phased roadmap (for implementation planning)

⸻

Phase 1 (MVP)
	•	CLI:
	•	tu, tu <name> [args...]
	•	--register, --unregister, --rename, --show, --list
	•	Registry:
	•	JSON schema v1 with type, target, description, timestamps.
	•	Environment variable override for path.
	•	Resolution:
	•	Registry lookup + dotted-name rule for unregistered names with ..
	•	Collision detection with no overwrites.
	•	Execution:
	•	Shell, python_module, python_callable.
	•	Python API:
	•	list_commands, register_command, unregister_command, rename_command, run.

Phase 2
	•	Global options framework and built-in --subshell.
	•	More complete completion support for names.
	•	Early error messages and fuzzy suggestions for unknown commands.

Phase 3
	•	Help store and capture (--capture-help, --edit-help).
	•	Help search (--search-help).
	•	Possible argument-level completion for some commands based on help analysis.

	13.	Design risks, trade-offs, and research keywords

⸻

Potential weaknesses / trade-offs
	•	The dotted-name rule is convenient but introduces asymmetry:
	•	Unregistered dotted names behave differently from undotted ones.
	•	This could surprise users if not well-documented.
	•	Single global JSON registry:
	•	Simple, but less friendly for:
	•	Multi-machine setups.
	•	Project-local overrides.
	•	Future extension to support project-local registries and layering may be desirable.
	•	The decision to disallow overwrites:
	•	It protects against accidental loss, but may annoy users who expect re-register to “just work”.
	•	Good error messages and ergonomics around rename/unregister are critical.
	•	Shell vs. Python-executed commands:
	•	Using subprocess for Python modules (via python -m) mirrors user reality, but sacrifices some potential introspection and integration opportunities compared to in-process execution.
	•	python_callable signature:
	•	Using callable(args: list[str]) keeps tu thin but may be limiting for richer CLI semantics; there is a tension between being a generic runner and imposing an interface.

Keywords for further exploration
	•	Command dispatcher / command bus
	•	CLI router / command registry
	•	Pluggable CLI, command palette
	•	“Interface-oriented design”, “interface-to-interface”
	•	“Software Design for Flexibility”, generic operators, combinators
	•	Domain-specific language (DSL) for commands
	•	Configuration-as-code, registry-as-DSL
	•	Unix philosophy, single entrypoint tools (e.g. git-style subcommands)
	•	Shell completion frameworks (bash-completion, zsh completion, fish completions)
	•	XDG base directory specification (for config and data locations)

This specification should be sufficient for an AI coding agent to implement a first version of tu that is small, composable, and aligned with the idea-to-implementation and interface-to-interface principles, while leaving room for future refinement and expansion.