#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code1 = """
$test_with_at: @(param $x:; $x * 2);
"""

test_code2 = """
$test_without_at: (param $x:; $x * 2);
"""

print("=== TESTING WITH @ SIGIL ===")
try:
    ast = parse(test_code1)
    result = eval_ast(ast)
    print(f"Success: {result}")
    print(f"Type: {type(_env['$test_with_at'])}")
    print(f"Value: {_env['$test_with_at']}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING WITHOUT @ SIGIL ===")
try:
    ast = parse(test_code2)
    result = eval_ast(ast)
    print(f"Success: {result}")
    print(f"Type: {type(_env.get('$test_without_at', 'NOT_FOUND'))}")
    print(f"Value: {_env.get('$test_without_at', 'NOT_FOUND')}")
except Exception as e:
    print(f"ERROR: {e}")
