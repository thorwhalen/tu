"""Shell completion support for tu."""

import os
import sys
from pathlib import Path
from typing import Optional

from .registry import list_commands


def get_completion_candidates(partial: str) -> list[str]:
    """Get command name candidates for completion.

    Args:
        partial: Partial command name typed by user.

    Returns:
        List of matching command names.
    """
    commands = list_commands()
    candidates = [cmd.name for cmd in commands if cmd.name.startswith(partial)]
    return sorted(candidates)


# All tu flags for completion
TU_FLAGS = [
    "--help",
    "--list",
    "--filter",
    "--show",
    "--register",
    "--unregister",
    "--rename",
    "--name",
    "--type",
    "--description",
    "--tags",
    "--force-dot-name",
    "--aliases",
    "--depends-on",
    "--env",
    "--timeout",
    "--subshell",
    "--dry-run",
    "--verbose",
    "--timeout-override",
    "--log",
    "--complete",
    "--completion-script",
    "--install-completion",
    "--export",
    "--import",
    "--merge",
    "--validate",
    "--stats",
    "--history",
    "--history-limit",
    "--interactive",
]


def get_flag_candidates(partial: str) -> list[str]:
    """Get flag candidates for completion.

    Args:
        partial: Partial flag typed by user (e.g. '--n' or '--').

    Returns:
        List of matching flags.
    """
    return sorted(f for f in TU_FLAGS if f.startswith(partial))


BASH_COMPLETION_SCRIPT = """
# Bash completion for tu
_tu_completion() {
    local cur prev
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Complete flags
    if [[ "$cur" == -* ]]; then
        local flags=$(tu --complete-flags="$cur" 2>/dev/null)
        COMPREPLY=( $(compgen -W "$flags" -- "$cur") )
        return 0
    fi

    # Complete command names for first positional argument
    if [ $COMP_CWORD -eq 1 ]; then
        local candidates=$(tu --complete "$cur" 2>/dev/null)
        COMPREPLY=( $(compgen -W "$candidates" -- "$cur") )
        return 0
    fi

    # Complete command names after certain flags
    case "$prev" in
        --show|--unregister|--validate)
            local candidates=$(tu --complete "$cur" 2>/dev/null)
            COMPREPLY=( $(compgen -W "$candidates" -- "$cur") )
            return 0
            ;;
        --type)
            COMPREPLY=( $(compgen -W "shell python_module python_callable" -- "$cur") )
            return 0
            ;;
        --completion-script|--install-completion)
            COMPREPLY=( $(compgen -W "bash zsh fish" -- "$cur") )
            return 0
            ;;
    esac

    # Default to file completion for arguments
    COMPREPLY=( $(compgen -f -- "$cur") )
    return 0
}

complete -F _tu_completion tu
"""


ZSH_COMPLETION_SCRIPT = r"""#compdef tu

# Zsh completion for tu - supports command names, flags, and menu selection
# Install: tu --install-completion zsh

_tu() {
    local -a commands flags

    # Get registered command names dynamically
    commands=(${(f)"$(tu --complete '' 2>/dev/null)"})

    flags=(
        '--help[Show help message and exit]'
        '-h[Show help message and exit]'
        '--list[List all registered commands]'
        '-l[List all registered commands]'
        '--filter[Filter commands by pattern]:pattern:'
        '--show[Show details of a command]:command name:($commands)'
        '--register[Register a new command]'
        '--unregister[Unregister a command]:command name:($commands)'
        '--rename[Rename a command]:old name:($commands):new name:'
        '--name[Name for the registered command]:name:'
        '--type[Type of command]:type:(shell python_module python_callable)'
        '--description[Description of the command]:description:'
        '--tags[Comma-separated tags]:tags:'
        '--force-dot-name[Allow dotted names without confirmation]'
        '--aliases[Comma-separated aliases]:aliases:'
        '--depends-on[Comma-separated dependencies]:deps:($commands)'
        '--env[KEY=VALUE environment variables]:env:'
        '--timeout[Timeout in seconds]:seconds:'
        '--subshell[Run command in a subdirectory]:directory:_directories'
        '--dry-run[Show what would execute without running]'
        '--verbose[Show detailed execution information]'
        '-v[Show detailed execution information]'
        '--timeout-override[Override command timeout]:seconds:'
        '--log[Write command output to log file]'
        '--completion-script[Print completion script]:shell:(bash zsh fish)'
        '--install-completion[Install completion for shell]:shell:(bash zsh fish)'
        '--export[Export registry to a file]:file:_files'
        '--import[Import registry from a file]:file:_files'
        '--merge[Merge when importing]'
        '--validate[Validate commands]:command name:($commands)'
        '--stats[Show registry statistics]'
        '--history[Show command history]:command name:($commands)'
        '--history-limit[Number of history entries]:limit:'
        '--interactive[Enter interactive REPL mode]'
        '-i[Enter interactive REPL mode]'
    )

    _arguments -s \
        $flags \
        '1:command:($commands)' \
        '*:args:_files'
}

_tu "$@"
"""


FISH_COMPLETION_SCRIPT = """
# Fish completion for tu
function __fish_tu_complete_commands
    tu --complete (commandline -ct) 2>/dev/null
end

function __fish_tu_needs_command
    set -l cmd (commandline -opc)
    test (count $cmd) -eq 1
end

# Command names
complete -c tu -f -n '__fish_tu_needs_command' -a '(__fish_tu_complete_commands)'

# Flags (available everywhere)
complete -c tu -l help -s h -d 'Show help message and exit'
complete -c tu -l list -s l -d 'List all registered commands'
complete -c tu -l filter -r -d 'Filter commands by pattern'
complete -c tu -l show -r -a '(__fish_tu_complete_commands)' -d 'Show command details'
complete -c tu -l register -d 'Register a new command'
complete -c tu -l unregister -r -a '(__fish_tu_complete_commands)' -d 'Unregister a command'
complete -c tu -l name -r -d 'Name for the registered command'
complete -c tu -l type -r -a 'shell python_module python_callable' -d 'Type of command'
complete -c tu -l description -r -d 'Description of the command'
complete -c tu -l tags -r -d 'Comma-separated tags'
complete -c tu -l force-dot-name -d 'Allow dotted names'
complete -c tu -l aliases -r -d 'Comma-separated aliases'
complete -c tu -l depends-on -r -d 'Dependencies'
complete -c tu -l env -r -d 'Environment variables'
complete -c tu -l timeout -r -d 'Timeout in seconds'
complete -c tu -l subshell -r -F -d 'Run in subdirectory'
complete -c tu -l dry-run -d 'Show what would execute'
complete -c tu -l verbose -s v -d 'Verbose output'
complete -c tu -l timeout-override -r -d 'Override timeout'
complete -c tu -l log -d 'Log command output'
complete -c tu -l completion-script -r -a 'bash zsh fish' -d 'Print completion script'
complete -c tu -l install-completion -r -a 'bash zsh fish' -d 'Install completion'
complete -c tu -l export -r -F -d 'Export registry'
complete -c tu -l import -r -F -d 'Import registry'
complete -c tu -l merge -d 'Merge when importing'
complete -c tu -l validate -a '(__fish_tu_complete_commands)' -d 'Validate commands'
complete -c tu -l stats -d 'Show statistics'
complete -c tu -l history -a '(__fish_tu_complete_commands)' -d 'Show history'
complete -c tu -l history-limit -r -d 'History entry limit'
complete -c tu -l interactive -s i -d 'Interactive REPL mode'
"""


def get_completion_script(shell: str) -> str:
    """Get completion script for a specific shell.

    Args:
        shell: Shell name (bash, zsh, fish).

    Returns:
        Completion script content.

    Raises:
        ValueError: If shell is not supported.
    """
    scripts = {"bash": BASH_COMPLETION_SCRIPT, "zsh": ZSH_COMPLETION_SCRIPT, "fish": FISH_COMPLETION_SCRIPT}
    if shell not in scripts:
        raise ValueError(f"Unsupported shell: {shell}. Supported: {', '.join(scripts)}")
    return scripts[shell]


# ---------------------------------------------------------------------------
# Completion installation
# ---------------------------------------------------------------------------

def _detect_shell() -> str:
    """Detect the current shell."""
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    elif "bash" in shell:
        return "bash"
    return "zsh"  # default on macOS


def _find_zsh_completion_dir() -> Path:
    """Find the best directory to install zsh completions.

    Checks (in order):
    1. oh-my-zsh completions dir
    2. ~/.zsh/completion (conventional user dir)
    3. /usr/local/share/zsh/site-functions (system, may need sudo)
    """
    # oh-my-zsh
    omz = Path.home() / ".oh-my-zsh" / "completions"
    if omz.parent.is_dir():
        return omz

    # User-local conventional dir
    return Path.home() / ".zsh" / "completion"


def _find_bash_completion_dir() -> Path:
    """Find directory for bash completions."""
    # Check common locations
    for d in [
        Path.home() / ".bash_completion.d",
        Path("/etc/bash_completion.d"),
        Path("/usr/local/etc/bash_completion.d"),
    ]:
        if d.is_dir():
            return d
    return Path.home() / ".bash_completion.d"


def _find_fish_completion_dir() -> Path:
    """Find directory for fish completions."""
    return Path.home() / ".config" / "fish" / "completions"


def _get_completion_install_path(shell: str) -> Path:
    """Get the target path for installing completion for a given shell."""
    if shell == "zsh":
        return _find_zsh_completion_dir() / "_tu"
    elif shell == "bash":
        return _find_bash_completion_dir() / "tu"
    elif shell == "fish":
        return _find_fish_completion_dir() / "tu.fish"
    else:
        raise ValueError(f"Unsupported shell: {shell}")


def is_completion_installed(shell: Optional[str] = None) -> bool:
    """Check whether the tu completion script is installed for the given shell."""
    if shell is None:
        shell = _detect_shell()
    try:
        path = _get_completion_install_path(shell)
        return path.is_file()
    except ValueError:
        return False


def install_completion(shell: str, yes: bool = False) -> str:
    """Install the completion script for the given shell.

    Finds the appropriate directory, asks for confirmation, writes the file.

    Args:
        shell: Shell name (bash, zsh, fish).
        yes: Skip confirmation prompt.

    Returns:
        Status message describing what was done.
    """
    script = get_completion_script(shell)
    target = _get_completion_install_path(shell)

    # Show what we're about to do
    action = "Overwrite" if target.is_file() else "Create"
    print(f"{action}: {target}")

    if not yes:
        try:
            response = input("Proceed? [Y/n] ")
        except (EOFError, KeyboardInterrupt):
            return "\nInstallation cancelled."
        if response.strip().lower() in ("n", "no"):
            return "Installation cancelled."

    # Write the file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(script)

    # Shell-specific post-install notes
    extra = ""
    if shell == "zsh":
        # Check if the dir is in fpath (via oh-my-zsh or manual config)
        omz_dir = Path.home() / ".oh-my-zsh"
        if not omz_dir.is_dir() and "~/.zsh/completion" not in os.environ.get("FPATH", ""):
            extra = (
                "\n\nNote: You may need to add this to your ~/.zshrc:\n"
                "    fpath=(~/.zsh/completion $fpath)\n"
                "    autoload -Uz compinit && compinit"
            )
        extra += "\n\nRestart your shell or run: exec zsh"
    elif shell == "bash":
        extra = "\n\nRestart your shell or run: source ~/.bashrc"
    elif shell == "fish":
        extra = ""  # fish auto-loads from completions dir

    return f"Completion installed to {target}{extra}"


def check_completion_hint() -> Optional[str]:
    """Return a hint string if completion is not installed, else None.

    Uses a stamp file to avoid nagging on every invocation — shows the hint
    at most once per day.
    """
    shell = _detect_shell()

    if is_completion_installed(shell):
        return None

    # Rate-limit: check at most once per day using a stamp file
    stamp = Path.home() / ".config" / "tu" / ".completion_hint_stamp"
    if stamp.is_file():
        import time
        age = time.time() - stamp.stat().st_mtime
        if age < 86400:  # 24 hours
            return None

    # Update stamp
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.touch()

    return (
        f"Tip: Enable tab-completion for tu by running:\n"
        f"    tu --install-completion {shell}\n"
    )
