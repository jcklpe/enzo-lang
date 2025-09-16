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

// Simplified bubble sort with tracing
bubble-sort: (
    param $list: [];
    param $order: "ascending";

    "Starting bubble sort with list:" then print;
    $list then print;

    $length: $list then $get-length;
    "List length:" then print;
    $length then print;

    // Just do one pass to see what happens
    $current-index: 1;
    $max-index: $length - 1;

    "Starting inner loop, max-index:" then print;
    $max-index then print;

    Loop while $current-index is at most $max-index, (
        $next-index: $current-index + 1;

        "Comparing indices:" then print;
        $current-index then print;
        $next-index then print;

        $current-element: $list.$current-index;
        $next-element: $list.$next-index;

        "Current element:" then print;
        $current-element then print;
        "Next element:" then print;
        $next-element then print;

        $should-swap: False;

        If $order is "ascending", (
            If $current-element is greater than $next-element, (
                "Should swap (ascending)!" then print;
                $should-swap <: True;
            );
        );

        If $should-swap, (
            "Before swap - list:" then print;
            $list then print;

            // Swap elements
            $next-element :> $list.$current-index;
            $current-element :> $list.$next-index;

            "After swap - list:" then print;
            $list then print;
        ), Else, (
            "No swap needed" then print;
        );

        $current-index + 1 :> $current-index;
    );

    "Final list before return:" then print;
    $list then print;

    return($list);
);

// Test with a simple case
$test-numbers: [64, 34, 25];
"Original test numbers:" then print;
$test-numbers then print;

$result: $bubble-sort($test-numbers, "ascending");
"Returned result:" then print;
$result then print;

"Test numbers after function call:" then print;
$test-numbers then print;
'''

print("=== BUBBLE SORT TRACE DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    if result is not None:
        print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
