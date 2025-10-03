#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Test with string-based flags first
"Testing string assignment:";
$test-var: "false";
$test-var;

$test-var <: "true";
$test-var;

"Testing comparison:";
$a: 64;
$b: 34;
$a;
$b;

"Testing conditional assignment with strings:";
$should-swap: "false";
$should-swap;

If $a is greater than $b, (
    "Inside if block - should set to true";
    $should-swap <: "true";
    "After assignment, should-swap is:";
    $should-swap;
);

"Outside if block, should-swap is:";
$should-swap;

"Now testing with built-in variants:";
$should-swap-variant: False;
$should-swap-variant;

If $a is greater than $b, (
    "Inside if block - should set to True variant";
    $should-swap-variant <: True;
    "After assignment, should-swap-variant is:";
    $should-swap-variant;
);

"Outside if block, should-swap-variant is:";
$should-swap-variant;
'''

print("=== TESTING TRUE/FALSE ASSIGNMENTS ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()