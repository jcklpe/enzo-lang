#!/usr/bin/env python3

from src.enzo_parser.tokenizer import Tokenizer

code = '''If $status-if,
    "Ready!";
end;'''

print("=== DEBUGGING CONTROL FLOW TOKENIZATION ===")
print(f"Code: {code}")

tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()

print("\n=== TOKENS ===")
for i, token in enumerate(tokens):
    print(f"Token {i}: {token}")
