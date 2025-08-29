---
applyTo: "**"
---
# Project general coding standards

# Rules you must always follow
- Never ever change a test case or golden file without explicitly consulting me and getting the go ahead, even if the test case has a typo or something that doesn't follow spec and makes it fail.

## Important Context
- The interpreter can be found in folder `~/work/enzo-lang/interpreter/`. `enzo-lang/` is the root project folder but all terminal commands for the interpreter must be run from the interpreter folder.
- you import the tokenizer with the name `Tokenizer`, NOT `tokenize.
- You can import a parser for debug files rather than creating a custom one using `from src.enzo_parser.parser import parse`
- The interpreter project is a poetry env so you have to use `poetry run python` instead of just `python`
- please put all debugging related scripts in the "debugging" folder so it doesn't clutter the project space. If you need to debug something it might be helpful to check if a script already exists there too.
- All error messaging and all error handling are centralized to the "error_messaging.py" and "error_handling.py" files.
- When running tests remember this legend at the top of the test runner output:
```
✔ correct expected outcome
✖ failing actual outcome
```
### Debugging and Import Guidelines

- **Always check existing imports**: Before writing debug scripts, look at how other files import from the same modules. Use `grep_search` to find existing import patterns.
- **Verify exports before importing**: Use `read_file` or `grep_search` to check what classes/functions are actually exported from a module before trying to import them.
- **Follow established patterns**: Look at existing debug scripts in the `debugging/` folder for reference on correct import patterns.
- **Common import patterns in this project**:
  - `from src.evaluator import eval_ast, _env, _initialize_builtin_variants`
  - `from src.enzo_parser.parser import parse` (not a class, just the parse function)
  - `from src.error_handling import EnzoRuntimeError, EnzoTypeError, EnzoParseError`

### Before creating debug scripts:
1. Check existing debug scripts for import patterns
2. Use `grep_search` to find how the target module is imported elsewhere
3. Use `read_file` to verify class/function names if unsure

# Interpreter technical context:
## Import and Module Context
```
# Evaluator imports
from src.evaluator import eval_ast
from src.evaluator import _env  # Global environment (NOT global_env)

# Parser imports
from src.enzo_parser.parser import parse
from src.enzo_parser.ast_nodes import (
    # Common nodes
    Binding, BindOrRebind, VarInvoke, NumberAtom, TextAtom, ListAtom,
    # Control flow
    IfStatement, LoopStatement, EndLoopStatement, RestartLoopStatement,
    # Other nodes as needed
)

# Error handling imports
from src.error_handling import (
    EnzoRuntimeError, EnzoTypeError, EnzoParseError,
    ReturnSignal, EndLoopSignal, RestartLoopSignal
)
```
### Common Import Patterns

### Key Module Exports

- `src.evaluator`: exports `eval_ast()` function and `_env` (global environment)
- `src.enzo_parser.parser`: exports `parse()` function
- `src.enzo_parser.ast_nodes`: exports all AST node classes
- `src.error_handling`: exports all error classes and signal classes

### Debugging Setup

- Always use `poetry run python` instead of `python`
- Put debugging scripts in the `debugging/` folder
- Always begin commands with `cd /Users/aslan/work/enzo-lang/interpreter` to make sure you are in the right folder.
- Common debugging pattern:
```
import sys
sys.path.append('..')  # If needed to import from parent
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()  # IMPORTANT: Re-add True, False, Status variants

# Parse and evaluate test code
ast = parse(test_code)
result = eval_ast(ast)
```

### Environment Management Warning
- **NEVER** call `_env.clear()` without immediately calling `_initialize_builtin_variants()`
- The global environment `_env` contains essential built-in variant groups (`True`, `False`, `Status`) that Enzo code depends on
- Clearing without re-initializing will cause "undefined variable" errors when code references `True` or `False`

### Function Signatures to Remember
- `eval_ast(node, env=None, value_demand=False, is_function_context=False, outer_env=None)`
- `parse(code_string)` returns Program AST node

# Misc
- Enzo doesn't have boolean literals. Enzo does not have a dedicated boolean type. Enzo has custom types, with Blueprints for product types, and Blueprint variant groups for sum types/ sum of product types. True and False are built in blueprint variant groups. They are not a dedicated type in enzo.
