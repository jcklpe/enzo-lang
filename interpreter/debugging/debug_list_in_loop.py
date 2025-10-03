#!/usr/bin/env python3
"""Test list rebinding in loops like bubble sort does."""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
$list: [3, 1, 2];
$i: 1;

Loop while $i is at most 2, (
    $temp: $list.$i;
    $list;
    $i + 1 :> $i;
);

$list;
'''

print("=== Testing list access in loop ===")
ast = parse(test_code)
result = eval_ast(ast)
print(f"Result: {result}")
print(f"List in env: {_env.get('list', 'NOT_FOUND')}")