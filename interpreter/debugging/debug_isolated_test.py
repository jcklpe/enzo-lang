#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== TESTING FUNCTION WITHOUT @ ===")
try:
    # Test what (param $x:; $x * 2) evaluates to
    result1 = eval_ast(parse('(param $x:; $x * 2);'))
    print(f"Function without @: {result1}")
    print(f"Type: {type(result1)}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING FUNCTION WITH @ ===")
try:
    # Test what @(param $x:; $x * 2) evaluates to
    result2 = eval_ast(parse('@(param $x:; $x * 2);'))
    print(f"Function with @: {result2}")
    print(f"Type: {type(result2)}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING anon_ref_apply DEFINITION ===")
try:
    # Define anon_ref_apply
    eval_ast(parse('''
    anon_ref_apply: (
        param $func: ();
        param $value: "";
        return( $func($value) );
    );
    '''))
    print("anon_ref_apply defined successfully")
except Exception as e:
    print(f"ERROR defining anon_ref_apply: {e}")

print("\n=== TESTING CALL WITH FUNCTION WITHOUT @ ===")
try:
    # Test the failing call
    result = eval_ast(parse('anon_ref_apply( (param $x:; $x * 2), 5 );'))
    print(f"Result: {result}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
