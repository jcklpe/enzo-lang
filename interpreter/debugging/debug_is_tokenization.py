#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.tokenizer import Tokenizer

# Test the specific case that's failing
test_code = "is-list-empty: ("

print("Testing tokenization of:", repr(test_code))
print()

tokenizer = Tokenizer(test_code)
try:
    tokens = tokenizer.tokenize()
    for i, token in enumerate(tokens):
        print(f"Token {i}: {token}")
except Exception as e:
    print(f"Error: {e}")

print()
print("Expected: The entire 'is-list-empty' should be tokenized as a KEYNAME, not split at 'is'")
