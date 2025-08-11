#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.tokenizer import Tokenizer

def debug_token_positions():
    test_code = """$list-pipe
then ($this contains 4) :> $contains-four;"""

    print("=== TEST CODE ===")
    print(repr(test_code))
    print("\n=== TOKENIZATION ===")

    tokenizer = Tokenizer(test_code)
    tokens = tokenizer.tokenize()

    # Filter out whitespace tokens
    filtered_tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]

    for i, token in enumerate(filtered_tokens):
        print(f"Token {i}: {token.type:15} '{token.value:10}' start={getattr(token, 'start', 'N/A'):3} end={getattr(token, 'end', 'N/A'):3}")

    print(f"\n=== SOURCE TEXT ANALYSIS ===")
    print(f"Source length: {len(test_code)}")
    print("Character positions:")
    for i, char in enumerate(test_code):
        if char == '\n':
            print(f"  {i:2}: '\\n'")
        else:
            print(f"  {i:2}: '{char}'")

if __name__ == "__main__":
    debug_token_positions()
