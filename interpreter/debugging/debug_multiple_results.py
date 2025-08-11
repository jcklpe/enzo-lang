#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Simpler test to see what results we get
test_code = '''
$x: 1;
$y: 2;
$x;
$y;
'''

print("=== Testing multiple statement results with parse_program ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
