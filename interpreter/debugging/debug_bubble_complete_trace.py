#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Helper to get list length
get-length: (
    param $list: [];
    $count: 0;
    Loop for $item in $list, (
        $count + 1 :> $count;
    );
    return($count);
);

// Test with a very simple 3-element array first
bubble-sort-complete: (
    param $list: [];
    param $order: "ascending";

    "=== ENTERING bubble-sort-complete ===";
    $list;
    $order;

    $length: $get-length($list);
    "Length calculated:";
    $length;

    If $length is less than 2, (
        "Length < 2, returning early";
        return($list);
    );

    "Length >= 2, continuing with sort";
    $result-list: $list;
    "Initial result-list:";
    $result-list;

    $pass: 1;
    $max-passes: $length - 1;
    "Max passes will be:";
    $max-passes;

    // Do fixed number of passes (n-1)
    Loop while $pass is at most $max-passes, (
        "=== PASS";
        $pass;
        "===";

        $position: 1;
        $max-position: $length - $pass + 1;
        "Max position for this pass:";
        $max-position;

        // One pass through adjacent elements
        Loop while $position is less than $max-position, (
            "  Position:";
            $position;

            $current: $result-list.$position;
            $next-pos: $position + 1;
            $next: $result-list.$next-pos;

            "  Current:";
            $current;
            "  Next:";
            $next;

            $should-swap: False;
            If $order is "ascending", (
                If $current is greater than $next, (
                    "  SHOULD SWAP (ascending)";
                    $should-swap <: True;
                );
            ), Else if $order is "descending", (
                If $current is less than $next, (
                    "  SHOULD SWAP (descending)";
                    $should-swap <: True;
                );
            );

            "  Should swap?";
            $should-swap;

            If $should-swap, (
                "  PERFORMING SWAP";
                // Use the same swapping logic that worked in single-pass
                $new-list: [];
                $rebuild-pos: 1;

                Loop while $rebuild-pos is at most $length, (
                    If $rebuild-pos is $position, (
                        $new-list <: [<$new-list>, $next];
                    ), Else if $rebuild-pos is $next-pos, (
                        $new-list <: [<$new-list>, $current];
                    ), Else, (
                        $elem: $result-list.$rebuild-pos;
                        $new-list <: [<$new-list>, $elem];
                    );
                    $rebuild-pos + 1 :> $rebuild-pos;
                );

                $new-list :> $result-list;
                "  After swap, result-list is now:";
                $result-list;
            ), Else, (
                "  NO SWAP NEEDED";
            );

            $position + 1 :> $position;
        );

        "End of pass";
        $pass;
        "result so far:";
        $result-list;
        $pass + 1 :> $pass;
    );

    "=== FINAL RESULT ===";
    $result-list;
    return($result-list);
);

// Test with simple 3-element array
$test: [64, 34, 25];
$test;
"Calling bubble-sort-complete...";
$result: $bubble-sort-complete($test, "ascending");
$result;
'''

print("=== DEBUGGING BUBBLE SORT COMPLETE FUNCTION ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()