#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def debug_comparison_values():
    print("Starting comparison debug...")
    _env.clear()
    _initialize_builtin_variants()

    test_code = '''
    $list: [3, 1, 2];
    "List is:";
    $list;

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

        // Show what we're comparing
        $prev-item;
        $current-item;

        If $prev-item is greater than $current-item, (
            "YES - should swap";
        ), Else, (
            "NO - should not swap";
        );
    );
    '''

    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print("Comparison debug completed successfully")
    except Exception as e:
        print(f"Error during debug: {e}")

if __name__ == "__main__":
    debug_comparison_values()