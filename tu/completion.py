"""Shell completion support for tu."""

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


BASH_COMPLETION_SCRIPT = """
# Bash completion for tu
_tu_completion() {
    local cur prev
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # If we're completing the first argument after 'tu'
    if [ $COMP_CWORD -eq 1 ]; then
        # Get completions from tu itself
        local candidates=$(tu --complete "$cur" 2>/dev/null)
        COMPREPLY=( $(compgen -W "$candidates" -- "$cur") )
        return 0
    fi

    # Default to file completion for arguments
    COMPREPLY=( $(compgen -f -- "$cur") )
    return 0
}

complete -F _tu_completion tu
"""


ZSH_COMPLETION_SCRIPT = """
#compdef tu

_tu_completion() {
    local -a candidates
    candidates=(${(f)"$(tu --complete ${words[2]} 2>/dev/null)"})
    _describe 'command' candidates
}

_tu_completion "$@"
"""


FISH_COMPLETION_SCRIPT = """
# Fish completion for tu
function __fish_tu_complete
    set -l cmd (commandline -opc)
    if test (count $cmd) -eq 1
        tu --complete (commandline -ct) 2>/dev/null
    end
end

complete -c tu -f -a '(__fish_tu_complete)'
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
    if shell == "bash":
        return BASH_COMPLETION_SCRIPT
    elif shell == "zsh":
        return ZSH_COMPLETION_SCRIPT
    elif shell == "fish":
        return FISH_COMPLETION_SCRIPT
    else:
        raise ValueError(f"Unsupported shell: {shell}")


def install_completion(shell: str) -> str:
    """Get installation instructions for completion.

    Args:
        shell: Shell name (bash, zsh, fish).

    Returns:
        Installation instructions.
    """
    script = get_completion_script(shell)

    if shell == "bash":
        return f"""To install bash completion for tu, add this to your ~/.bashrc:

{script}

Or save the script to a file and source it:
    tu --completion-script bash > ~/.tu-completion.bash
    echo 'source ~/.tu-completion.bash' >> ~/.bashrc
"""
    elif shell == "zsh":
        return f"""To install zsh completion for tu, save the script to your fpath:

    tu --completion-script zsh > ~/.zsh/completion/_tu

And make sure your ~/.zshrc contains:
    fpath=(~/.zsh/completion $fpath)
    autoload -Uz compinit && compinit
"""
    elif shell == "fish":
        return f"""To install fish completion for tu:

    tu --completion-script fish > ~/.config/fish/completions/tu.fish
"""
    else:
        raise ValueError(f"Unsupported shell: {shell}")
