#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.tokenizer import Tokenizer

def test_else_tokens():
    code = '''$status-else: "";

If $status-else, (
  "Won't print";
), Else, (
  "Fallback triggered";
);'''
    
    print(f"Code:\n{code}")
    print("\nTokens:")
    
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    
    for i, token in enumerate(tokens):
        if token.type not in ('WHITESPACE', 'NEWLINE'):
            print(f"  {i}: {token}")

if __name__ == "__main__":
    test_else_tokens()
