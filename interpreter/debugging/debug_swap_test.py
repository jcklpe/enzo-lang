#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

# Test just the swapping mechanism
test_code = '''
$test-list: [3, 1, 2];
$test-list;

$temp: $test-list.1;
$test-list.2 :> $test-list.1;
$temp :> $test-list.2;

$test-list;
'''

print("Testing simple swap mechanism:")
print("Expected: [3, 1, 2] -> [1, 3, 2] (swap positions 1 and 2)")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Done")
except Exception as e:
    print(f"Error: {e}")
