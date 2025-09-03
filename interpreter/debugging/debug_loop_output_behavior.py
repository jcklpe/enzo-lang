#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== TESTING LOOP OUTPUT BEHAVIOR ===")

# Test 1: Loop that produces output
print("\n--- Loop with output ---")
test_code1 = '''
Loop for $item in [1, 2, 3], (
    "Item: <$item>";
);
'''

ast1 = parse(test_code1)
result1 = eval_ast(ast1)
print(f"Result from loop with output: {result1}")

# Test 2: Loop that produces no output
print("\n--- Loop with no output ---")
test_code2 = '''
Loop for $item in [1, 2, 3], (
    $temp: $item + 1;  // just a binding, no output
);
'''

ast2 = parse(test_code2)
result2 = eval_ast(ast2)
print(f"Result from loop with no output: {result2}")

# Test 3: Empty loop (no iterations)
print("\n--- Empty loop ---")
test_code3 = '''
Loop for $item in [], (
    "Never prints";
);
'''

ast3 = parse(test_code3)
result3 = eval_ast(ast3)
print(f"Result from empty loop: {result3}")
