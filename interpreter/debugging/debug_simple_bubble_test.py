#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
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

// Extremely simple bubble sort - just one pass
simple-bubble: (
    param $list: [];

    $length: $get-length($list);
    $length;

    // Just do one comparison and swap if needed
    If $length is at least 2, (
        $first: $list.1;
        $second: $list.2;
        $first;
        $second;

        If $first is greater than $second, (
            "Should swap";
            $new-list: [$second, $first];
            return($new-list);
        );
    );

    "No swap needed";
    return($list);
);

$test-list: [64, 34];
$test-list;

$result: $simple-bubble($test-list);
$result;
'''

print("=== SIMPLE BUBBLE TEST ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Simple bubble test completed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
