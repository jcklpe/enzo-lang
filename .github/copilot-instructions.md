---
applyTo: "**"
---
# Project general coding standards

# Rules you must always follow
- Never ever change a test case or golden file without explicitly consulting me and getting the go ahead, even if the test case has a typo or something that doesn't follow spec and makes it fail.

## Important Context
- The interpreter can be found in folder `~/work/enzo-lang/interpreter/`. `enzo-lang/` is the root project folder but all terminal commands for the interpreter must be run from the interpreter folder.
- The interpreter project is a poetry env so you have to use `poetry run python` instead of just `python`
- please put all debugging related scripts in the "debugging" folder so it doesn't clutter the project space. If you need to debug something it might be helpful to check if a script already exists there too.
- All error messaging and all error handling are centralized to the "error_messaging.py" and "error_handling.py" files.
- When running tests remember this legend at the top of the test runner output:
```
✔ correct expected outcome
✖ failing actual outcome
```

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
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Parse and evaluate test code
ast = parse(test_code)
result = eval_ast(ast)
```

### Function Signatures to Remember

- `eval_ast(node, env=None, value_demand=False, is_function_context=False, outer_env=None)`
- `parse(code_string)` returns Program AST node
