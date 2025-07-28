import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse, parse_program
from src.evaluator import eval_ast
from src.runtime_helpers import format_val

# Test the difference between parse and parse_program for function atoms
code = """($foo: 99; $foo);"""

print("Code:")
print(repr(code))
print("\n--- Testing parse() ---")

try:
    parsed = parse(code)
    print(f"parse() result: {parsed}")
    print(f"Type: {type(parsed)}")
    result = eval_ast(parsed, value_demand=True)
    print(f"eval_ast result: {result}")
    if result is not None:
        print(f"Formatted: {format_val(result)}")
except Exception as e:
    print(f"Error with parse(): {e}")
    import traceback
    traceback.print_exc()

print("\n--- Testing parse_program() ---")

try:
    parsed_prog = parse_program(code)
    print(f"parse_program() result: {parsed_prog}")
    print(f"Type: {type(parsed_prog)}")
    result_prog = eval_ast(parsed_prog, value_demand=True)
    print(f"eval_ast result: {result_prog}")
    if result_prog is not None:
        print(f"Formatted: {format_val(result_prog)}")
except Exception as e:
    print(f"Error with parse_program(): {e}")
    import traceback
    traceback.print_exc()
