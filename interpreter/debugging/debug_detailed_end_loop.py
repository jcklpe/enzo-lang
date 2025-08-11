#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test for-loop with end-loop and detailed logging
test_code = '''
$numbers: [1, 2, 3, 4, 5];
"Starting loop";
Loop for $num in $numbers, (
    "Processing:";
    $num;
    If $num is 3, (
        "About to end loop";
        end-loop;
        "This should not print";
    );
    "Continuing after if";
);
"Loop finished";
'''

print("=== Detailed test of for-loop with end-loop ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print("All results:")
    for i, res in enumerate(result):
        print(f"  {i}: {res}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
