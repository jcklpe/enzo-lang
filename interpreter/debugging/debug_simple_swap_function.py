#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Simple function that just tries to swap first two elements
test-swap: (
    param $list: [];

    $first: $list.1;
    $second: $list.2;

    $second :> $list.1;
    $first :> $list.2;

    return($list);
);

// Test the swap function
$test-numbers: [64, 34, 25];
$test-numbers;

$result: $test-swap($test-numbers);
$result;

$test-numbers;
'''

print("=== SIMPLE SWAP IN FUNCTION DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    if result is not None:
        print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
