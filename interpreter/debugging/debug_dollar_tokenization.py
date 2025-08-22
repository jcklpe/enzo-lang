#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.tokenizer import Tokenizer

# Test tokenization of $foo vs $
test_cases = ['$foo', '$', '$ foo', '$()']

for case in test_cases:
    print(f"Test: '{case}'")
    tokenizer = Tokenizer(case)
    tokens = tokenizer.tokenize()
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type} -> '{token.value}'")
    print()
