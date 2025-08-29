#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import Parser
from src.enzo_parser.tokenizer import Tokenizer

# Test the specific problematic case
test_code = """$anon_ref_ops: [
    @(param $n: ; $n * 2), // Doubler
    @(param $n: ; $n * $n) // Squarer
];"""

print("=== TOKENIZING ===")
tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()
for i, token in enumerate(tokens):
    print(f"{i:2d}: {token}")

print("\n=== DEBUGGING PARSER STATE ===")

# Use the standard parse function instead of manually creating parser
from src.enzo_parser.parser import parse

try:
    ast = parse(test_code)
    print("SUCCESS!")
    print(ast)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
