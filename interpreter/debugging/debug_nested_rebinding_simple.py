#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
"=== TESTING NESTED REBINDING SCOPING BUG ===";

"Test 1: Simple rebinding in single If statement";
$test1: False;
"Initial test1:";
$test1;

If 64 is greater than 34, (
    "Inside if - rebinding test1 to True";
    $test1 <: True;
    "Inside if - test1 is now:";
    $test1;
);

"Outside if - test1 should be True:";
$test1;

"Test 2: Rebinding in nested If statements (bubble sort case)";
$test2: False;
$order: "ascending";
"Initial test2:";
$test2;

If $order is "ascending", (
    "Inside outer if - order is ascending";
    If 64 is greater than 34, (
        "Inside nested if - rebinding test2 to True";
        $test2 <: True;
        "Inside nested if - test2 is now:";
        $test2;
    );
    "Back in outer if - test2 should be True:";
    $test2;
);

"Outside all ifs - test2 should be True:";
$test2;
'''

print("=== TESTING NESTED REBINDING SCOPING ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()