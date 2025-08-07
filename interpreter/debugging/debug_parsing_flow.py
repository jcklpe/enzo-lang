#!/usr/bin/env python3

from src.enzo_parser.tokenizer import tokenize

# Debug the tokenization of the failing expression
test_code = "$loop-iteration % 2 is 0;"

print("=== TOKENIZATION ===")
tokens = tokenize(test_code)
for i, token in enumerate(tokens):
    print(f"{i}: {token}")

print("\n=== STEP BY STEP PARSING ===")
print("Expected flow:")
print("1. parse_comparison_expression() -> parse_term()")
print("2. parse_term() -> parse_factor()")
print("3. parse_factor() processes '$loop-iteration % 2' -> ModNode")
print("4. parse_term() returns ModNode to parse_comparison_expression()")
print("5. parse_comparison_expression() sees 'is' and processes comparison")

print("\nActual issue: parse_factor() is calling parse_atom() for right side of %")
print("parse_atom() is trying to parse '2 is 0' but fails on 'is'")
