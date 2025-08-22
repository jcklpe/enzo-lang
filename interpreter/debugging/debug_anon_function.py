#!/usr/bin/env python3

import sys
import os

# Add path for importing src modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SCRIPT_DIR, "..", "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from enzo_parser.parser import parse
from enzo_parser.tokenizer import Tokenizer

# Test simple anonymous function invocation
test_code = '$();'

print(f"Test code: {test_code}")
print()

try:
    # First check tokenization
    tokenizer = Tokenizer(test_code)
    tokens = tokenizer.tokenize()
    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type} -> '{token.value}'")
    print()

    # Then try parsing
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print("AST:", ast)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

# Test the problematic anonymous function
code = '''($foo: 99; $foo);'''

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
    print(f"Result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
