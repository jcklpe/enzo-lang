#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("=== STANDALONE VARIABLE TEST ===")
test_code = """
$x: 5;
$x;
"""

print("Test code:")
print(test_code)
print("\nParsing...")
ast = parse(test_code)
print("Executing...")
result = eval_ast(ast)
print(f"Final result: {result}")

print("\n" + "="*50)

print("\n=== STANDALONE VARIABLE IN FUNCTION TEST ===")
test_code2 = """
simple_func: (
    param $x: ;
    $x;
);

simple_func(5);
"""

print("Test code:")
print(test_code2)
print("\nParsing...")
ast2 = parse(test_code2)
print("Executing...")
result2 = eval_ast(ast2)
print(f"Final result: {result2}")
