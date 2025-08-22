#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.tokenizer import Tokenizer

# Test the exact problematic code
test_code = '(@foo: 99; $foo);'

print(f"Test code: {test_code}")
print()

tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()

print("Tokens:")
for i, token in enumerate(tokens):
    print(f"  {i}: {token.type} -> '{token.value}'")
