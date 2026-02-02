#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_lexer import EnzoLexer
from pygments.token import Token

lexer = EnzoLexer()

code = "5"

print(f"=== Tokenizing: {repr(code)} ===")
tokens = list(lexer.get_tokens(code))
for token_type, value in tokens:
    print(f"Token: {token_type}, Value: {repr(value)}")

print("\n=== Checking Token.Number hierarchy ===")
print(f"Token.Number: {Token.Number}")
print(f"Token.Number.Integer: {Token.Number.Integer}")
print(f"Token.Literal.Number.Integer: {Token.Literal.Number.Integer}")

code2 = "function(5);"
print(f"\n=== Tokenizing: {repr(code2)} ===")
tokens2 = list(lexer.get_tokens(code2))
for token_type, value in tokens2:
    if value.strip():
        print(f"Token: {token_type:40}, Value: {repr(value)}")
