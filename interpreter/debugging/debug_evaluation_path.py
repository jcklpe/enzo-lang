#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse
from src.enzo_parser.ast_nodes import Invoke, ListIndex

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== DEBUGGING EVALUATION PATH ===")

# Monkey patch eval_ast to add debug info
original_eval_ast = eval_ast

def debug_eval_ast(node, *args, **kwargs):
    if isinstance(node, (Invoke, ListIndex)):
        print(f"EVAL: {type(node).__name__}: {node}")
    try:
        result = original_eval_ast(node, *args, **kwargs)
        return result
    except Exception as e:
        if isinstance(node, (Invoke, ListIndex)):
            print(f"ERROR in {type(node).__name__}: {e}")
        raise

# Replace the function
import src.evaluator
src.evaluator.eval_ast = debug_eval_ast

# Now test the failing case
test_code = """
anon_ref_apply: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);

$my_func: (param $x:5; $x * 2);
anon_ref_apply( $my_func, "text" );
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"SUCCESS: {result}")
except Exception as e:
    print(f"FINAL ERROR: {e}")
