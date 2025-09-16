#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Test the exact same swap detection logic in isolation
"=== TESTING SWAP DETECTION ===";

$order: "ascending";
$current: 64;
$next: 34;

"Current:";
$current;
"Next:";
$next;
"Order:";
$order;

$should-swap: False;
"Initial should-swap:";
$should-swap;

"Checking condition: current > next for ascending";
$current is greater than $next;

If $order is "ascending", (
    "Inside order check for ascending";
    If $current is greater than $next, (
        "Inside greater than check - setting should-swap to True";
        $should-swap <: True;
        "After setting, should-swap is now:";
        $should-swap;
    );
    "After inner if, should-swap is:";
    $should-swap;
);

"Final should-swap value:";
$should-swap;

"=== NOW TEST THE IF CONDITION ===";
If $should-swap, (
    "SWAP WOULD BE PERFORMED";
), Else, (
    "NO SWAP - should-swap is falsy";
);
'''

print("=== TESTING SWAP DETECTION LOGIC ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()