#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Testing Basic Assignment vs Rebinding ===")

# Test basic assignment (should work)
print("--- Testing assignment ---")
test_assignment = '''
$new_var: "assigned_value";
$new_var;
'''

try:
    ast = parse(test_assignment)
    result = eval_ast(ast)
    print(f"Assignment result - new_var: {_env.get('new_var', 'NOT_FOUND')}")
except Exception as e:
    print(f"Assignment error: {e}")

# Test rebinding existing variable
print("\n--- Testing rebinding ---")
_env['existing_var'] = "original_value"
print(f"Before rebind - existing_var: {_env.get('existing_var')}")

test_rebinding = '''
$existing_var <: "rebind_value";
$existing_var;
'''

try:
    ast = parse(test_rebinding)
    result = eval_ast(ast)
    print(f"Rebinding result - existing_var: {_env.get('existing_var', 'NOT_FOUND')}")
except Exception as e:
    print(f"Rebinding error: {e}")
    import traceback
    traceback.print_exc()