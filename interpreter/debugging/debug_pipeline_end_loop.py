#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test the pipeline end-loop error case
test_code = '''
Loop, (
    1 then (end-loop;);
);
'''

print("=== Testing end-loop in pipeline ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✖ No error thrown - this should have failed!")
    print(f"Result: {result}")

except Exception as e:
    print(f"✓ Correct error thrown: {e}")
    print(f"Error type: {type(e).__name__}")
