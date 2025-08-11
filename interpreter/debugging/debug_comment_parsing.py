#!/usr/bin/env python3

import sys
sys.path.append('src')

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser

def debug_comment_parsing():
    # Test with the exact string from the test file including comment
    code_with_comment = '''If $status-if,
  "Ready!"; // should print "Ready!"
end;'''

    print("=== DEBUGGING COMMENT PARSING ===")
    print(f"Code:\n{repr(code_with_comment)}")

    # Test tokenization
    print("\n=== TOKENIZATION ===")
    tokenizer = Tokenizer(code_with_comment)
    tokens = tokenizer.tokenize()
    clean_tokens = [t for t in tokens if t.type not in ['WHITESPACE', 'NEWLINE']]

    for i, token in enumerate(clean_tokens):
        print(f"{i}: {token}")

    # Test parsing with detailed error info
    print("\n=== PARSING ===")
    try:
        parser = Parser(code_with_comment)
        print(f"Parser created, tokens: {len(parser.tokens)}")

        # Debug the parse_if_statement step by step
        print("Starting parse...")

        # Check first token should be IF
        first_token = parser.peek()
        print(f"First token: {first_token}")

        if first_token and first_token.type == "IF":
            print("✅ Found IF token, calling parse_if_statement")
            ast = parser.parse()
            print(f"✅ SUCCESS: {ast}")
        else:
            print(f"❌ Expected IF token, got {first_token}")

    except Exception as e:
        print(f"❌ PARSE ERROR: {e}")
        print(f"Parser position: {parser.pos}")
        if parser.pos < len(parser.tokens):
            print(f"Current token: {parser.tokens[parser.pos]}")
            print(f"Remaining tokens: {parser.tokens[parser.pos:parser.pos+3]}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_comment_parsing()
