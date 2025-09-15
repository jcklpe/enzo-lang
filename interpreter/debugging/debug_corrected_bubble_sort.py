#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def debug_corrected_bubble_sort():
    # Reset environment
    _env.clear()
    _initialize_builtin_variants()

    # Test with the corrected bubble sort logic
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
                    "SWAPPING:";
                    ["Before swap:", $list];
                    ["Swapping positions", $prev-index, "and", $current-index];
                    ["Values:", $list.$prev-index, "and", $list.$current-index];

                    // Capture both values before swapping
                    $temp-prev: $list.$prev-index;
                    $temp-current: $list.$current-index;
                    // Swap the positions
                    $temp-current :> $list.$prev-index;
                    $temp-prev :> $list.$current-index;
                    $swapped <: True;

                    ["After swap:", $list];
                    // Update prev-item to the new value at current position
                    $temp-prev :> $prev-item;
                ), Else, (
                    $current-item :> $prev-item;
                );

                $current-index :> $prev-index;
            );
            ["End of pass, list:", $list];
        );

        return($list);
    );

    $test: [3, 1, 2];
    "Starting with:";
    $test;
    bubble-sort($test, "ascending") :> $result;
    "Final result:";
    $result;
    '''

    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print("Debug completed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_corrected_bubble_sort()
