#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== TESTING ERROR CASE 1 ===")
test_code = """
anon_ref_apply: (
    param $func: ();
    param $value: 0;
    return( $func($value) );
);

anon_ref_apply( (param $x:5; $x * 2), "text" );
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Unexpected success: {result}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")

print("\n=== TESTING ERROR CASE 2 ===")
test_code2 = """
$anon_ref_bad_syntax: @(param $x: $x + );
"""

try:
    ast = parse(test_code2)
    result = eval_ast(ast)
    print(f"Unexpected success: {result}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
