#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.tokenizer import Tokenizer

def test_tokenization():
    test_cases = [
        'If $status-if, ("Ready!");',
        'If true, ("yes");',
        'If $x, ("yes"); Else, ("no");'
    ]

    for i, code in enumerate(test_cases, 1):
        print(f"\nTest {i}: {code}")
        try:
            tokenizer = Tokenizer(code)
            tokens = tokenizer.tokenize()
            for j, token in enumerate(tokens):
                if token.type not in ('WHITESPACE', 'COMMENT'):  # Skip whitespace and comments for clarity
                    print(f"  {j}: {token}")
        except Exception as e:
            print(f"❌ Tokenization error: {e}")

if __name__ == "__main__":
    test_tokenization()
