#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_lexer import EnzoLexer

lexer = EnzoLexer()

code = '"text test";'

print(f"=== Tokenizing: {repr(code)} ===")
tokens = list(lexer.get_tokens(code))
for token_type, value in tokens:
    if value.strip():
        print(f"Token: {str(token_type):40}, Value: {repr(value)}")
