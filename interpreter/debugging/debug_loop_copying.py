#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_loop_behavior():
    # Reset environment
    _env.clear()
    _initialize_builtin_variants()

    # Test how loop variables work with copying
    test_code = '''
$test-list: [1, 2, 3];
$index: 0;

Loop for $item in $test-list, (
    $index + 1 :> $index;
    "Index <$index>: item is <$item>";

    // Try to modify the item
    $item + 10 :> $item;
    "Modified item is now <$item>";

    // Try to put it back in the list
    $item :> $test-list.$index;
);

$test-list;
    '''

    print("Testing loop behavior:")
    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print(f"Final result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_loop_behavior()
