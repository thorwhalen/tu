# tu.options

Global options framework for tu.

### Functions

| [`apply_global_options`](#tu.options.apply_global_options)(plan, options)   | Apply global options to an execution plan.         |
|----------------------------------------------------------------------------------------|----------------------------------------------------|
| [`subshell_option`](#tu.options.subshell_option)(plan, remaining_args) | Transform execution plan to run in a subdirectory. |

### tu.options.apply_global_options(plan, options)

Apply global options to an execution plan.

* **Parameters:**
  * **plan** ([`ExecutionPlan`](tu.models.html.md#tu.models.ExecutionPlan)) – Initial execution plan.
  * **options** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Dictionary of option names to their argument lists.
* **Return type:**
  [`ExecutionPlan`](tu.models.html.md#tu.models.ExecutionPlan)
* **Returns:**
  Transformed execution plan.

### tu.options.subshell_option(plan, remaining_args)

Transform execution plan to run in a subdirectory.

* **Parameters:**
  * **plan** ([`ExecutionPlan`](tu.models.html.md#tu.models.ExecutionPlan)) – Current execution plan.
  * **remaining_args** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Remaining arguments (first should be the directory).
* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`ExecutionPlan`](tu.models.html.md#tu.models.ExecutionPlan), [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  Tuple of (modified ExecutionPlan, remaining args without directory).
