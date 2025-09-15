#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Test the get-list-length function with a simple case
test_code = """
get-list-length: (
    param $list: [];
    $count: 0;
    $index: 1;

    Loop, (
        If $list.$index is Empty, (
            end-loop;
        );
        $count + 1 :> $count;
        $index + 1 :> $index;
    );

    return($count);
);

$test: [1, 2, 3];
get-list-length($test);
"""

print("Testing get-list-length function:")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test simple list bounds checking
test_bounds = """
$test: [1, 2, 3];
$test.1;
$test.2;
$test.3;
$test.4;
"""

print("Testing list bounds:")
try:
    ast2 = parse(test_bounds)
    result2 = eval_ast(ast2)
    print(f"Result: {result2}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test empty list behavior
test_empty = """
$empty: [];
$empty.1;
"""

print("Testing empty list access:")
try:
    ast3 = parse(test_empty)
    result3 = eval_ast(ast3)
    print(f"Result: {result3}")
except Exception as e:
    print(f"Error: {e}")
