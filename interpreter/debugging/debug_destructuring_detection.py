#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import EnzoParser
from src.enzo_parser.tokenizer import tokenize

# Test the exact case that's failing
test_code = "[@(param $n: ; $n * 2)]"

print("=== Tokenizing the full test case ===")
tokens = tokenize(test_code)
for i, token in enumerate(tokens):
    print(f"{i}: {token}")

print("\n=== Simulating parser state when it reaches '$n * 2' ===")
# When we get to parsing the body of the function atom, we would have consumed:
# LBRACK, AT, LPAR, PARAM, KEYNAME($n), BIND, SEMICOLON
# So the parser would be positioned at the KEYNAME($n) for the body statement

body_tokens = [
    ('KEYNAME', '$n'),
    ('MUL', '*'),
    ('NUMBER', '2'),
    ('RPAR', ')'),
    ('RBRACK', ']')
]

print("Starting from body statement '$n * 2':")
for i, (token_type, value) in enumerate(body_tokens):
    print(f"{i}: TokenType.{token_type}='{value}'")

print("\n=== Testing is_destructuring_pattern logic manually ===")

# Simulate the destructuring pattern check
# pos = 1 would be the MUL token
# pos = 2 would be the NUMBER token
# pos = 3 would be the RPAR token

# The key question: does is_destructuring_pattern return True for '$n * 2' sequence?

# Let's create a minimal parser state to test this
parser = EnzoParser(test_code)

# Advance to where we would be when parsing the function body
# We need to get past: LBRACK, AT, LPAR, PARAM, KEYNAME($n), BIND, SEMICOLON
target_pos = 7  # Should be at the KEYNAME($n) for the body
while parser.pos < target_pos and parser.pos < len(parser.tokens):
    parser.advance()

print(f"\nParser positioned at: {parser.peek()} (pos={parser.pos})")
print("Next few tokens:")
for i in range(5):
    token = parser.peek(i)
    if token:
        print(f"  peek({i}): {token}")
    else:
        print(f"  peek({i}): None")

print(f"\nCurrent token is KEYNAME: {parser.peek() and parser.peek().type == 'KEYNAME'}")
print(f"Next token is BIND: {parser.peek(1) and parser.peek(1).type == 'BIND'}")

# Test the is_destructuring_pattern function by simulating its logic
current_token = parser.peek()
if current_token and current_token.type == "KEYNAME":
    # Check if next token is BIND (this should return False for simple binding)
    if parser.peek(1) and parser.peek(1).type == "BIND":
        print("is_destructuring_pattern should return False (simple binding)")
    else:
        print("is_destructuring_pattern will scan ahead for comma patterns...")

        pos = 1
        found_comma = False
        bracket_depth = 0

        while parser.peek(pos) and pos < 20:
            token = parser.peek(pos)
            print(f"  Scanning pos {pos}: {token}")

            if token.type == "LBRACK":
                bracket_depth += 1
            elif token.type == "RBRACK":
                bracket_depth -= 1
            elif token.type == "COMMA" and bracket_depth == 0:
                found_comma = True
                print(f"    Found comma at pos {pos}")
            elif token.type == "BIND" and found_comma:
                print(f"    Found BIND after comma - returning True")
                break
            elif token.type == "ARROW" and found_comma:
                print(f"    Found ARROW after comma - returning True")
                break
            elif token.type == "VARIANTS":
                print(f"    Found VARIANTS - returning False")
                break
            elif token.type in ["SEMICOLON", "NEWLINE", "RBRACE"]:
                print(f"    Found statement end - breaking")
                break
            pos += 1

        if not found_comma:
            print("  No comma found - should return False")
        else:
            print("  Found comma but no BIND/ARROW after - should return False")
