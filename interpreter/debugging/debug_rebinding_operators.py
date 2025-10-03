#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
"=== COMPARING <: vs :> REBINDING IN IF STATEMENTS ===";

"Test A: Using <: rebinding in If statement";
$testA: False;
"Initial testA:";
$testA;

If 64 is greater than 34, (
    "Inside if - using <: to rebind testA";
    $testA <: True;
    "Inside if - testA is now:";
    $testA;
);

"Outside if - testA should be True:";
$testA;

"Test B: Using :> rebinding in If statement";
$testB: False;
"Initial testB:";
$testB;

If 64 is greater than 34, (
    "Inside if - using :> to rebind testB";
    True :> $testB;
    "Inside if - testB is now:";
    $testB;
);

"Outside if - testB should be True:";
$testB;

"Test C: Using :> in Loop (known to work)";
$testC: 0;
"Initial testC:";
$testC;

$nums: [1, 2];
Loop for $n in $nums, (
    "Inside loop - adding to testC";
    $testC + $n :> $testC;
    "Inside loop - testC is now:";
    $testC;
);

"Outside loop - testC should be 3:";
$testC;
'''

print("=== COMPARING REBINDING OPERATORS ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()