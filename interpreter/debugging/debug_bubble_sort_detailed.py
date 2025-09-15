#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Test with detailed debugging
test_code = '''
bubble-sort-debug: (
    param $list: [];
    param $order: "ascending";

    "Starting bubble sort with list:";
    $list;

    $swapped: True;
    $pass-count: 0;

    Loop while $swapped, (
        $pass-count + 1 :> $pass-count;
        "Pass number:";
        $pass-count;

        $swapped <: False;
        $prev-item: ;
        $prev-index: 0;
        $current-index: 0;

        Loop for $current-item in $list, (
            $current-index + 1 :> $current-index;

            "Current index:";
            $current-index;
            "Current item:";
            $current-item;

            If $current-index is 1, (
                "First item, setting prev";
                $current-item :> $prev-item;
                $current-index :> $prev-index;
                restart-loop;
            );

            "Prev item:";
            $prev-item;
            "Comparing prev > current:";
            $prev-item is greater than $current-item;

            $should-swap: False;
            If $order is "ascending", (
                If $prev-item is greater than $current-item, (
                    $should-swap <: True;
                    "SHOULD SWAP!";
                );
            );

            If $should-swap, (
                "SWAPPING positions";
                $prev-index;
                "and";
                $current-index;

                $current-item :> $list.$prev-index;
                $prev-item :> $list.$current-index;
                $swapped <: True;

                "List after swap:";
                $list;

                $current-item :> $prev-item;
            ), Else, (
                $current-item :> $prev-item;
            );

            $current-index :> $prev-index;
        );

        "End of pass, list is now:";
        $list;
    );

    return($list);
);

$test: [3, 1, 2];
bubble-sort-debug($test, "ascending") :> $result;
$result;
'''

print("Testing bubble sort with detailed debug output:")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Debug completed")
except Exception as e:
    print(f"Error: {e}")
