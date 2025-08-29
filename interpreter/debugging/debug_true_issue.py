#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()

print("Current environment keys:", list(_env.keys()))

# Test if True is defined
print("\nTesting True:")
try:
    result = eval_ast(parse("True;")[0])
    print("True result:", result)
except Exception as e:
    print("True error:", e)

# Test with hardcoded condition
print("\nTesting with literal condition:")
test = """
$x: "global";
If 1, (
    $x: "shadowed";
    $x;
);
$x;
"""

try:
    ast = parse(test)
    result = eval_ast(ast)
    print("SUCCESS with literal condition")
except Exception as e:
    print("ERROR with literal:", e)
