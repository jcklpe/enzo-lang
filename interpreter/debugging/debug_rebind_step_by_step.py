#!/usr/bin/env python3
"""Debug rebind step by step to understand the issue."""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Test 1: Simple rebind outside loop
print("=== Test 1: Simple rebind outside loop ===")
test1 = '''
$counter: 0
$counter + 1 :> $counter
$counter
'''
ast1 = parse(test1)
result1 = eval_ast(ast1)
print(f"Result: {result1} (should be 1)")

# Reset for test 2
_env.clear()
_initialize_builtin_variants()

# Test 2: One iteration manually
print("\n=== Test 2: One loop iteration manually ===")
test2 = '''
$counter: 0;
$active-while: True;
If $active-while, (
    $counter + 1 :> $counter;
    False :> $active-while;
);
$counter;
'''
ast2 = parse(test2)
result2 = eval_ast(ast2)
print(f"Result: {result2} (should be 1)")
print(f"Active-while in env: {'active-while' in _env}")
print(f"All keys: {list(_env.keys())}")
print(f"Active-while: {_env.get('active-while', 'NOT_FOUND')} (should be False)")