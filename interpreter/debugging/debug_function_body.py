#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import Parser
from src.enzo_parser.tokenizer import Tokenizer

# Test the specific problematic case
test_code = """@(param $n: ; $n * 2)"""

print("=== TOKENIZING ===")
tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()
for i, token in enumerate(tokens):
    print(f"{i:2d}: {token}")

print("\n=== MANUAL STEP THROUGH ===")
# Let's manually see what happens in function parsing
print("Starting from @ token...")
print("After (, we have PARAM token...")
print("The function body after ; should be: $n * 2")

# Let's see what the function parser does
# from src.enzo_parser.parser_function import parse_function_atom

# Find tokens after semicolon
semicolon_pos = None
for i, token in enumerate(tokens):
    if token.type == "SEMICOLON":
        semicolon_pos = i
        break

if semicolon_pos:
    print(f"\nTokens after semicolon (the function body):")
    for i in range(semicolon_pos + 1, len(tokens)):
        if tokens[i].type == "RPAR":
            break
        print(f"  {i}: {tokens[i]}")
