"""Global options framework for tu."""

from typing import Callable

from .models import ExecutionPlan


# Type for global option transformers
GlobalOptionTransformer = Callable[[ExecutionPlan, list[str]], tuple[ExecutionPlan, list[str]]]


def subshell_option(plan: ExecutionPlan, remaining_args: list[str]) -> tuple[ExecutionPlan, list[str]]:
    """Transform execution plan to run in a subdirectory.

    Args:
        plan: Current execution plan.
        remaining_args: Remaining arguments (first should be the directory).

    Returns:
        Tuple of (modified ExecutionPlan, remaining args without directory).
    """
    if not remaining_args:
        raise ValueError("--subshell requires a directory argument")

    directory = remaining_args[0]
    remaining_args = remaining_args[1:]

    # Create new plan with updated cwd
    new_plan = ExecutionPlan(
        command_type=plan.command_type,
        target=plan.target,
        args=plan.args,
        cwd=directory,
        env=plan.env
    )

    return new_plan, remaining_args


# Registry of global options
GLOBAL_OPTIONS: dict[str, GlobalOptionTransformer] = {
    "subshell": subshell_option,
}


def apply_global_options(
    plan: ExecutionPlan,
    options: dict[str, list[str]]
) -> ExecutionPlan:
    """Apply global options to an execution plan.

    Args:
        plan: Initial execution plan.
        options: Dictionary of option names to their argument lists.

    Returns:
        Transformed execution plan.
    """
    current_plan = plan

    for option_name, option_args in options.items():
        if option_name not in GLOBAL_OPTIONS:
            raise ValueError(f"Unknown global option: --{option_name}")

        transformer = GLOBAL_OPTIONS[option_name]
        current_plan, _ = transformer(current_plan, option_args)

    return current_plan
