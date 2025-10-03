#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Helper function to get the length of a list
get-length: (
    param $list: [];
    $length: 0;
    Loop for $item in $list, (
        $length + 1 :> $length;
    );
    return($length);
);

// Test the actual bubble sort logic with one manual iteration
$test-list: [64, 34, 25];
$test-list;

$length: $test-list then $get-length;
$length;

// Manual first pass of bubble sort
$current-pass: 1;
$current-index: 1;
$max-index: $length - $current-pass;
$max-index;

// First comparison: index 1 vs 2 (64 vs 34)
$current-element: $test-list.$current-index;
$current-element;

$next-index: $current-index + 1;
$next-element: $test-list.$next-index;
$next-element;

$should-swap: $current-element is greater than $next-element;
$should-swap;

// If should swap, do the swap
$temp-current: $current-element;
$temp-next: $next-element;

$temp-next :> $test-list.$current-index;
$temp-current :> $test-list.$next-index;

$test-list;
'''

print("=== MANUAL BUBBLE SORT STEP DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    if result is not None:
        print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
