#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.tokenizer import Tokenizer

# Test just the comment line itself
test_cases = [
    "//= IF CONDITION WITH NESTED LIST INDEX ACCESS",
    "// regular comment",
    "//=another test section",
    "//normal comment",
    "$var: 5; //= inline comment test"
]

for i, code in enumerate(test_cases):
    print(f"\n=== TEST CASE {i+1}: {repr(code)} ===")
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()

    for token in tokens:
        if token.type != "WHITESPACE":
            print(f"  {token.type:15s} {repr(token.value)} at {token.start}-{token.end}")

    comment_tokens = [t for t in tokens if t.type == "COMMENT"]
    if comment_tokens:
        print(f"  -> Found {len(comment_tokens)} comment token(s)")
    else:
        print(f"  -> NO COMMENT TOKENS FOUND!")

print(f"\n=== TESTING THE ACTUAL PROBLEMATIC TEXT ===")
problematic_text = '''$goblinoid.status;  // should print "dead"

//= IF CONDITION WITH NESTED LIST INDEX ACCESS
$nested-list: [["zero", "one"], ["two", "three"]];'''

print("Problematic text:")
print(repr(problematic_text))
print()

tokenizer = Tokenizer(problematic_text)
tokens = tokenizer.tokenize()

print("All tokens including whitespace:")
for i, token in enumerate(tokens):
    print(f"{i:2d}: {token.type:15s} {repr(token.value)} at {token.start}-{token.end}")

print("\nComment tokens:")
comment_tokens = [t for t in tokens if t.type == "COMMENT"]
for token in comment_tokens:
    print(f"  {repr(token.value)} at {token.start}-{token.end}")

if not comment_tokens:
    print("  NO COMMENT TOKENS FOUND!")
    print("  Checking character by character in the gap...")
    # Find the gap where the comment should be
    for i in range(len(problematic_text)):
        if problematic_text[i:i+2] == "//":
            end = problematic_text.find('\n', i)
            if end == -1:
                end = len(problematic_text)
            comment_line = problematic_text[i:end]
            print(f"  Found '//' at position {i}: {repr(comment_line)}")
