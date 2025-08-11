#!/usr/bin/env python3
"""Debug spread syntax parsing"""

import sys
sys.path.append('..')
from src.enzo_parser.lexer import tokenize

# Test the problematic syntax
test_code = '''[<$dynamic-list>, 3] :> $dynamic-list;'''

print("Testing spread syntax...")
print(f"Code: {test_code}")
print("Tokens:")

try:
    tokens = tokenize(test_code)
    for i, token in enumerate(tokens):
        print(f"{i}: {token.type} = '{token.value}'")
except Exception as e:
    print(f"Tokenization error: {e}")
