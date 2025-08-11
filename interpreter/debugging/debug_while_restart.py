#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test while loop with restart-loop
test_code = '''
$i-99: 0;
$processed-99: 0;
Loop while $i-99 is less than 5, (
    $i-99 + 1 :> $i-99;
    "Processing i =";
    $i-99;
    If $i-99 is 3, (
        "Restarting loop, skipping processing";
        restart-loop;
    );
    $processed-99 + 1 :> $processed-99;
    "Processed count is now:";
    $processed-99;
);
"Final i:";
$i-99;
"Final processed:";
$processed-99;
'''

print("=== Testing while loop with restart-loop ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print("Results:")
    for i, res in enumerate(result):
        print(f"  {i}: {res}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
