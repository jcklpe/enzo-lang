#!/usr/bin/env python3

import sys
sys.path.append('src')

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser

def debug_if_parsing():
    code = '''$status-if: "ready";

If $status-if,
  "Ready!";
end;'''

    print("=== DEBUGGING IF BLOCK PARSING ===")
    print(f"Code:\n{code}")

    # Tokenize
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    clean_tokens = [t for t in tokens if t.type not in ['WHITESPACE', 'NEWLINE']]

    print(f"\n=== TOKENS ===")
    for i, token in enumerate(clean_tokens):
        print(f"{i}: {token}")

    # Parse step by step
    parser = Parser(code)
    try:
        print(f"\n=== PARSING ===")
        ast = parser.parse()
        print(f"Success: {ast}")
    except Exception as e:
        print(f"Parse error: {e}")
        print(f"Current token index: {parser.pos}")
        if parser.pos < len(parser.tokens):
            print(f"Current token: {parser.tokens[parser.pos]}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_if_parsing()
