#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

print("=== Testing Function Atom Scoping ===")

# Test 1: Basic function atom scoping
print("\n1. Basic function atom scoping:")
test1 = """
$x: "global";
$func: (
    $x: "function-local";
    $x;
);
$func;
$x;
"""

try:
    ast1 = parse(test1)
    result1 = eval_ast(ast1)
    print("Function atom result:", result1)
except Exception as e:
    print("Function atom error:", e)
    import traceback
    traceback.print_exc()

# Reset environment
_env.clear()

print("\n2. Function atom variable leakage test:")
test2 = """
$func: (
    $local_var: "should not leak";
    $local_var;
);
$func;
$local_var;
"""

try:
    ast2 = parse(test2)
    result2 = eval_ast(ast2)
    print("Unexpected success - should error")
except Exception as e:
    print("Expected error:", e)

# Reset environment
_env.clear()

print("\n3. Direct comparison - function atom vs conditional:")
test3a = """
$x: "global";
$direct_func: (
    $x: "shadowed";
    $x;
);
$direct_func;
"""

test3b = """
$x: "global";
If True, (
    $x: "shadowed";
    $x;
);
"""

print("Function atom version:")
try:
    ast3a = parse(test3a)
    result3a = eval_ast(ast3a)
    print("Function atom success:", result3a)
except Exception as e:
    print("Function atom error:", e)

_env.clear()

print("Conditional version:")
try:
    ast3b = parse(test3b)
    result3b = eval_ast(ast3b)
    print("Conditional success:", result3b)
except Exception as e:
    print("Conditional error:", e)
