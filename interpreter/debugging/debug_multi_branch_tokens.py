#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.tokenizer import Tokenizer

def test_multi_branch_tokens():
    code = '''If $switch-val either is "A", (
  "A";),
or is "B", (
  "B matched";);'''
    
    print(f"Code:\n{code}")
    print("\nTokens:")
    
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    
    for i, token in enumerate(tokens):
        if token.type not in ('WHITESPACE', 'NEWLINE'):
            print(f"  {i}: {token}")

if __name__ == "__main__":
    test_multi_branch_tokens()
