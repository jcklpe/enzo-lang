#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def debug_bubble_sort():
    # Reset environment
    _env.clear()
    _initialize_builtin_variants()

    # Test with a simple 3-element list to trace the algorithm
    test_code = '''
bubble-sort: (
    param $list: [];
    param $order: "ascending";

    $swapped: True;

    Loop while $swapped, (
        $swapped <: False;
        $prev-item: ;
        $prev-index: 0;
        $current-index: 0;

        Loop for $current-item in $list, (
            $current-index + 1 :> $current-index;

            If $current-index is 1, (
                $current-item :> $prev-item;
                $current-index :> $prev-index;
                restart-loop;
            );

            $should-swap: False;

            If $order is "ascending", (
                If $prev-item is greater than $current-item, (
                    $should-swap <: True;
                );
            ), Else, (
                If $prev-item is less than $current-item, (
                    $should-swap <: True;
                );
            );

            If $should-swap, (
                $current-item :> $list.$prev-index;
                $prev-item :> $list.$current-index;
                $swapped <: True;
                $current-item :> $prev-item;
            ), Else, (
                $current-item :> $prev-item;
            );

            $current-index :> $prev-index;
        );
    );

    return($list);
);

$test: [3, 1, 2];
$test;
bubble-sort($test, "ascending") :> $result;
$result;
    '''

    print("Testing bubble sort with [3, 1, 2]:")
    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print(f"Final result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_bubble_sort()
