#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Debugging Rebinding Logic ===")

# Let's trace what environments are being passed
test_code = '''
$test_var: "original";
$test_var;
'''

# First set up the variable
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Initial setup - test_var: {_env.get('test_var')}")
    print(f"Global env keys: {list(_env.keys())}")
except Exception as e:
    print(f"Setup Error: {e}")

# Now test the rebinding directly
print("\n--- Testing direct rebinding ---")
test_rebind = '''
$test_var <: "directly_changed";
$test_var;
'''

try:
    ast = parse(test_rebind)
    result = eval_ast(ast)
    print(f"After direct rebind - test_var: {_env.get('test_var')}")
except Exception as e:
    print(f"Direct rebind error: {e}")

# Reset
_env['test_var'] = "original"
print(f"\nReset test_var to: {_env.get('test_var')}")

# Test rebinding in function atom
print("\n--- Testing function atom rebinding ---")
test_func_rebind = '''
($x: 1; $test_var <: "changed_by_function"; "debug");
$test_var;
'''

try:
    ast = parse(test_func_rebind)
    result = eval_ast(ast)
    print(f"After function rebind - test_var: {_env.get('test_var')}")
except Exception as e:
    print(f"Function rebind error: {e}")
    import traceback
    traceback.print_exc()