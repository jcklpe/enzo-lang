#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test for-loop with end-loop
test_code = '''
$numbers: [1, 2, 3, 4, 5];
Loop for $num in $numbers, (
    $num;
    If $num is 3, (end-loop;);
);
'''

print("=== Testing for-loop with end-loop ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print(f"Results: {result}")
    print("Expected: [1, 2, 3]")

    # Should only get numbers 1, 2, 3
    expected = [1, 2, 3]
    if result == expected:
        print("✓ Correct!")
    else:
        print("✖ Wrong - end-loop not working properly")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
