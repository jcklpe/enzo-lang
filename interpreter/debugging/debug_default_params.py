#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== TESTING FUNCTION WITH DEFAULT PARAMS ===")
try:
    # Test a function with default parameter values
    result = eval_ast(parse('(param $x: 0; $x * 2);'))
    print(f"Function with default param: {result}")
    print(f"Type: {type(result)}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING FUNCTION WITH NO DEFAULT PARAMS ===")
try:
    # Test a function without default parameter values
    result = eval_ast(parse('(param $x:; $x * 2);'))
    print(f"Function without default param: {result}")
    print(f"Type: {type(result)}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING anon_ref_apply WITH FUNCTION WITH DEFAULTS ===")
try:
    # Define anon_ref_apply
    eval_ast(parse('''
    anon_ref_apply: (
        param $func: ();
        param $value: "";
        return( $func($value) );
    );
    '''))

    # Test calling with a function that has default params
    result = eval_ast(parse('anon_ref_apply( (param $x: 0; $x * 2), 5 );'))
    print(f"Result: {result}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
