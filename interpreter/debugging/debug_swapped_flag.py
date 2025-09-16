#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Test the $swapped flag behavior
get-length: (
    param $list: [];
    $count: 0;
    Loop for $item in $list, (
        $count + 1 :> $count;
    );
    return($count);
);

debug-swapped-loop: (
    param $list: [];

    $length: $get-length($list);
    "Length:";
    $length;

    $result-list: $list;
    $swapped: True;
    "Initial swapped:";
    $swapped;

    $outer-iteration: 0;

    Loop while $swapped, (
        $outer-iteration + 1 :> $outer-iteration;
        "=== Pass";
        $outer-iteration;

        $swapped <: False;
        "Reset swapped to:";
        $swapped;

        $position: 1;

        Loop while $position is less than $length, (
            $current: $result-list.$position;
            $next-pos: $position + 1;
            $next: $result-list.$next-pos;

            "Comparing";
            $current;
            "vs";
            $next;

            If $current is greater than $next, (
                "SHOULD SWAP!";
                $swapped <: True;
                "Set swapped to:";
                $swapped;
                // Skip actual swapping for now to focus on flag logic
            );

            $position + 1 :> $position;
        );

        "End of pass, swapped is:";
        $swapped;

        If $outer-iteration is greater than 5, (
            "Safety break - too many iterations";
            return($result-list);
        );
    );

    "Final result:";
    return($result-list);
);

$test: [64, 34, 25];
$debug-swapped-loop($test);
'''

print("=== DEBUG SWAPPED FLAG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Debug completed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
