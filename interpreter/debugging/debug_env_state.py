#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

# Let's add some debug prints to understand what's happening
# First let me test if the variable exists in the outer environment

test_code = '''
$should_swap: False;
$should_swap;
'''

print("=== TESTING SIMPLE VARIABLE DECLARATION ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result after initial declaration: {result}")
    print(f"_env contents: {dict(_env)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Now test simple rebinding outside If statement
test_code2 = '''
$should_swap <: True;
$should_swap;
'''

print("\n=== TESTING SIMPLE REBINDING ===")
try:
    ast = parse(test_code2)
    result = eval_ast(ast)
    print(f"Result after simple rebinding: {result}")
    print(f"_env contents: {dict(_env)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()