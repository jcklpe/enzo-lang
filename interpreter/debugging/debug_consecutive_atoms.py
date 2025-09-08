#!/usr/bin/env python3
"""Debug script to trace parsing of consecutive function atoms"""

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse
from src.enzo_parser.tokenizer import Tokenizer

# Test the problematic code
test_code = "(4+4); (5+6); // prints 8 then 10"
print(f"Testing code: {test_code}")
print()

# First let's see the tokens WITH positions
print("=== TOKENIZATION WITH POSITIONS ===")
tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()
for i, token in enumerate(tokens):
    if token.type not in ("NEWLINE", "COMMENT", "SKIP"):
        print(f"{i}: {token.type} = '{token.value}' at pos {token.start}-{token.end}")

print()
print("=== CHARACTER POSITIONS ===")
for i, char in enumerate(test_code):
    print(f"{i}: '{char}'")

print()

# Now let's try to parse
print("=== PARSING ===")
try:
    ast = parse(test_code)
    print(f"AST type: {type(ast)}")
    print(f"AST: {ast}")
    if hasattr(ast, 'statements'):
        print(f"Number of statements: {len(ast.statements)}")
        for i, stmt in enumerate(ast.statements):
            print(f"Statement {i}: {type(stmt)} = {stmt}")
except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()
