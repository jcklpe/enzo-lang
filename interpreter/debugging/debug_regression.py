import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast
from src.runtime_helpers import format_val

# Test case from "Function atom with single variable and implicit return"
code = """($foo: 99; $foo);"""

print("Code:")
print(code)
print("\nParsing and evaluating:")

try:
    parsed = parse(code)
    print(f"Parsed successfully")
    print(f"AST: {parsed}")
    result = eval_ast(parsed, value_demand=True)
    print(f"Result: {result}")
    if result is not None:
        print(f"Formatted: {format_val(result)}")
    else:
        print("Result is None - this is the problem!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
