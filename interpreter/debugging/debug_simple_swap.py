#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def debug_simple_swap():
    # Reset environment
    _env.clear()
    _initialize_builtin_variants()

    # Test simple swapping
    test_code = '''
    $test: [3, 1, 2];
    "Before swap:";
    $test;

    // Try to swap positions 1 and 2
    $temp: $test.1;
    $test.2 :> $test.1;
    $temp :> $test.2;

    "After swap:";
    $test;
    '''

    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print("Simple swap test completed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_simple_swap()
