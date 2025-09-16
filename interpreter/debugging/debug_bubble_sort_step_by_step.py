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

// Test basic function calls first
$test-list: [64, 34, 25];
$test-list;

$list-length: $test-list then $get-length;
$list-length;

// Test basic list access
$first: $test-list.1;
$first;

$second: $test-list.2;
$second;

// Test basic comparison
$comparison-result: $first is greater than $second;
$comparison-result;

// Test basic assignment to list indices
$test-list.1;
99 :> $test-list.1;
$test-list.1;
$test-list;
'''

print("=== BASIC OPERATIONS DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    if result is not None:
        print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
