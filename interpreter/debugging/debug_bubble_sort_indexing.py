#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Test the get-list-length function first
test_code = """
get-list-length: (
    param $list: [];
    $count: 0;
    $index: 1;

    Loop, (
        If $list.$index is empty, (
            end-loop;
        );
        $count + 1 :> $count;
        $index + 1 :> $index;
    );

    return($count);
);

$test-list: [1, 2, 3];
$length: get-list-length($test-list);
$length;
"""

print("Testing get-list-length function:")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test simple list access first
test_code2 = """
$list: [64, 34, 25];
$list.1;
$list.2;
$list.3;
"""

print("Testing basic list access:")
try:
    ast2 = parse(test_code2)
    result2 = eval_ast(ast2)
    print(f"Result: {result2}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test what happens when we access index 4 (out of range)
test_code3 = """
$list: [64, 34, 25];
$list.4;
"""

print("Testing out of range access (should error):")
try:
    ast3 = parse(test_code3)
    result3 = eval_ast(ast3)
    print(f"Result: {result3}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test Empty check
test_code4 = """
$list: [1, 2, 3];
$first: $list.1;
If $first is Empty, (
    "first is empty";
), Else, (
    "first is not empty";
);
"""

print("Testing Empty check:")
try:
    ast4 = parse(test_code4)
    result4 = eval_ast(ast4)
    print(f"Result: {result4}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test accessing beyond list length
test_code5 = """
$list: [1, 2, 3];
$beyond: $list.4;
If $beyond is Empty, (
    "beyond is empty";
), Else, (
    "beyond is not empty";
);
"""

print("Testing access beyond list length:")
try:
    ast5 = parse(test_code5)
    result5 = eval_ast(ast5)
    print(f"Result: {result5}")
except Exception as e:
    print(f"Error: {e}")
