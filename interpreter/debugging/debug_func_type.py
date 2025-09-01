#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== DEBUGGING WHAT $func CONTAINS ===")

test_code = """
anon_ref_apply: (
    param $func: ();
    param $value: "";
    If $func is Function, ( "func is Function" );
    If $func is List, ( "func is List" );
    $func;  // Just return the function to see what it is
);

$my_func: (param $x:5; $x * 2);
anon_ref_apply( $my_func, "text" );
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
    print(f"Type: {type(result)}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
