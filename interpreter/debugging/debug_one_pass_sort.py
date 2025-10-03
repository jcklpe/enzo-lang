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

// Simplified bubble sort - just one pass
bubble-sort-one-pass: (
    param $list: [];
    param $order: "ascending";

    $length: $list then $get-length;

    $current-index: 1;
    $max-index: $length - 1;

    Loop while $current-index is at most $max-index, (
        $next-index: $current-index + 1;
        $current-element: $list.$current-index;
        $next-element: $list.$next-index;

        $should-swap: False;

        If $order is "ascending", (
            If $current-element is greater than $next-element, (
                $should-swap <: True;
            );
        );

        If $should-swap, (
            // Swap elements
            $next-element :> $list.$current-index;
            $current-element :> $list.$next-index;
        );

        $current-index + 1 :> $current-index;
    );

    return($list);
);

// Test the one-pass function
$test-numbers: [64, 34, 25];
$test-numbers;

$result: $bubble-sort-one-pass($test-numbers, "ascending");
$result;

// Check if original was modified
$test-numbers;
'''

print("=== ONE PASS BUBBLE SORT DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    if result is not None:
        print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
