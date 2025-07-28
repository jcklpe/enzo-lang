#!/usr/bin/env python3

import sys
import os

# Add path for importing src modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SCRIPT_DIR, "..", "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser

# Test the problematic multi-branch sequence
code = '''$switch-val: "B";

If $switch-val either is "A",
  "A";
or is "B",
  "B matched";
end;'''

print("Code:")
print(code)
print("\nTokens:")
tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()

for i, token in enumerate(tokens):
    if token.type not in ["WHITESPACE", "NEWLINE"]:
        print(f"{i:2d}: {token}")

print("\nParsing:")
try:
    parser = Parser(code)
    ast = parser.parse()
    print("Success!")
    print(ast)
except Exception as e:
    print(f"Error: {e}")
    # Get more details if possible
    import traceback
    traceback.print_exc()
