#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def debug_values():
    _env.clear()
    _initialize_builtin_variants()

    # Test basic comparisons first
    test_code = '''
    $a: 3;
    $b: 1;
    $a;
    $b;
    If $a is greater than $b, (
        "3 is greater than 1 - CORRECT";
    ), Else, (
        "3 is NOT greater than 1 - WRONG";
    );
    '''

    print("Testing basic comparison:")
    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print(f"Basic comparison result: {result}")
    except Exception as e:
        print(f"Error in basic comparison: {e}")

    # Test the actual bubble sort values
    test_code2 = '''
    $list: [3, 1, 2];
    $first: $list.1;
    $second: $list.2;
    $first;
    $second;
    If $first is greater than $second, (
        "First is greater - should swap";
    ), Else, (
        "First is not greater - should not swap";
    );
    '''

    print("\nTesting list values:")
    try:
        ast2 = parse(test_code2)
        result2 = eval_ast(ast2)
        print(f"List comparison result: {result2}")
    except Exception as e:
        print(f"Error in list comparison: {e}")

if __name__ == "__main__":
    debug_values()
