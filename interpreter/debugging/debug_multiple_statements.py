#!/usr/bin/env python3

import sys
import os

# Add path for importing src modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SCRIPT_DIR, "..", "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

# Test multiple statements like in the failing test
code = '''$a: 3;
$a;
$b: 3;
$b;
($foo: 2; $foo);'''

print("Code:")
print(code)

print("\nParsing and evaluating:")
try:
    parser = Parser(code)
    ast = parser.parse()
    print("Parsed successfully")
    print("AST:", ast)

    # Evaluate
    result = eval_ast(ast)
    print(f"Final result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
