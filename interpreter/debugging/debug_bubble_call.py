#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Test if bubble-sort is being called at all
bubble-sort: (
    param $list: [];
    param $order: "ascending";

    "BUBBLE SORT WAS CALLED!";
    $list;

    // Return a completely different list to see if it's used
    $fake-sorted: [999, 888, 777];
    return($fake-sorted);
);

$numbers: [64, 34, 25];
"Before:";
$numbers;

$bubble-sort($numbers, "ascending") :> $numbers;
"After:";
$numbers;
'''

print("=== BUBBLE SORT CALL TEST ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Test completed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
