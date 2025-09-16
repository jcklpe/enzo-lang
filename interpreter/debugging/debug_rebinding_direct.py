#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Direct test of the bubble sort rebinding issue
$should_swap: False;
$order: "ascending";

If $order is "ascending", (
    If 64 is greater than 34, (
        $should_swap <: True;
    );
);

$should_swap;
'''

print("=== DIRECT TEST OF BUBBLE SORT REBINDING ISSUE ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
    print("Expected: True")
    print(f"Test {'PASSED' if result == 'True' else 'FAILED'}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()