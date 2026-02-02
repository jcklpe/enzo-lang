#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_lexer import EnzoLexer
from pygments.token import Token

lexer = EnzoLexer()

code = """function: (
param $x: 5;
return($x + 5);
);"""

print("=== Tokenizing ===")
print(code)
print("\n=== Tokens ===")

tokens = list(lexer.get_tokens(code))
for i, (token_type, value) in enumerate(tokens):
    print(f"{i:3d}. {str(token_type):40} | {repr(value)}")

print("\n=== Looking for closing parens ===")
for i, (token_type, value) in enumerate(tokens):
    if value == ')':
        print(f"Line {i}: Token type: {token_type}, Value: {repr(value)}")
