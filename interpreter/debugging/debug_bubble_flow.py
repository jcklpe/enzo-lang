#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def debug_bubble_flow():
    _env.clear()
    _initialize_builtin_variants()

    # Simplified version with explicit debug output
    test_code = '''
    bubble-sort-debug: (
        param $list: [];

        "Starting bubble sort";
        $list;

        $pass: 0;
        $swapped: True;

        Loop while $swapped, (
            $pass + 1 :> $pass;
            ["Pass", $pass];
            $swapped <: False;
            $prev-item: ;
            $prev-index: 0;
            $current-index: 0;

            Loop for $current-item in $list, (
                $current-index + 1 :> $current-index;
                ["Loop iteration:", $current-index, "item:", $current-item];

                If $current-index is 1, (
                    "Setting first item as prev";
                    $current-item :> $prev-item;
                    $current-index :> $prev-index;
                    restart-loop;
                );

                ["Comparing:", $prev-item, "vs", $current-item];

                If $prev-item is greater than $current-item, (
                    "Should swap!";
                    $prev-item;
                    $current-item;
                    $list.$prev-index;
                    $list.$current-index;

                    // Do the actual swap
                    $temp-prev: $list.$prev-index;
                    $temp-current: $list.$current-index;
                    $temp-current :> $list.$prev-index;
                    $temp-prev :> $list.$current-index;
                    $swapped <: True;

                    "After swap:";
                    $list;
                );

                $current-item :> $prev-item;
                $current-index :> $prev-index;
            );

            ["End of pass", $pass, "result:", $list];
            If $pass is greater than 5, (
                "Safety break";
                $swapped <: False;
            );
        );

        return($list);
    );

    $test: [3, 1, 2];
    bubble-sort-debug($test) :> $result;
    "Final:";
    $result;
    '''

    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print("Bubble sort debug completed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_bubble_flow()
