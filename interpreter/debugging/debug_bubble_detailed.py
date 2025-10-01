#!/usr/bin/env python3
"""Test simplified bubble sort to find the index error."""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

_env.clear()
_initialize_builtin_variants()

test_code = '''
get-length: (
    param $list: [];
    $count: 0;
    Loop for $item in $list, (
        $count + 1 :> $count;
    );
    return($count);
);

bubble-sort: (
    param $list: [];

    $length: get-length($list);
    "Starting bubble sort, length: <$length>";

    If $length is less than 2, (
        return($list);
    );

    $current-list: $list;
    $pass: 1;

    // Just do one pass
    Loop while $pass is at most 1, (
        "Pass <$pass>, current-list: <$current-list>";
        $position: 1;

        Loop while $position is less than $length, (
            "Position <$position>/<$length>";
            $current-elem: $current-list.$position;
            $next-elem: $current-list.($position + 1);

            If $current-elem is greater than $next-elem, (
                "Should swap <$current-elem> and <$next-elem>";
                $new-list: [];
                $rebuild-pos: 1;

                Loop while $rebuild-pos is at most $length, (
                    If $rebuild-pos is $position, (
                        $new-list <: [<$new-list>, $next-elem];
                    ), Else if $rebuild-pos is ($position + 1), (
                        $new-list <: [<$new-list>, $current-elem];
                    ), Else, (
                        $elem: $current-list.$rebuild-pos;
                        $new-list <: [<$new-list>, $elem];
                    );
                    $rebuild-pos + 1 :> $rebuild-pos;
                );

                "New list: <$new-list>";
                $new-list :> $current-list;
                "After swap, current-list: <$current-list>";
            );

            $position + 1 :> $position;
        );

        $pass + 1 :> $pass;
    );

    return($current-list);
);

$result: bubble-sort([3, 1, 2]);
"Result: <$result>";
'''

print("=== Testing bubble sort with detailed output ===")
ast = parse(test_code)
result = eval_ast(ast)
print(f"Final result: {result}")
