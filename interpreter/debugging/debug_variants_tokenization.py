#!/usr/bin/env python3

from src.enzo_parser.tokenizer import Tokenizer

code = 'Monster2 variants:'

print("=== DEBUGGING TOKENIZATION ===")
print(f"Code: {code}")

tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()

print("\n=== TOKENS ===")
for i, token in enumerate(tokens):
    print(f"Token {i}: {token}")
