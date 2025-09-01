#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = """
anon_ref_apply: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);

$test_func_with_at: @(param $x:; $x * 2);
$test_func_without_at: (param $x:; $x * 2);

// Test the function types
If $test_func_with_at is Function, ( "WITH @ is Function" );
If $test_func_without_at is Function, ( "WITHOUT @ is Function" );

// Test calling anon_ref_apply with each
anon_ref_apply( $test_func_with_at, 5 );
"""

print("=== TESTING FUNCTION TYPES AND CALLS ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Success: {result}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nNow testing the direct call that fails...")

test_code2 = """
anon_ref_apply: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);

anon_ref_apply( (param $x:; $x * 2), 5 );
"""

try:
    ast = parse(test_code2)
    result = eval_ast(ast)
    print(f"Success: {result}")
except Exception as e:
    print(f"ERROR: {e}")
