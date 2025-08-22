#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.enzo_parser.tokenizer import Tokenizer
from src.error_handling import EnzoParseError

# Test the problematic multiline function call
test_code = """$(@x: 101;
@y: 100;
return($x + $y););"""

print(f"Test code:")
print(test_code)
print()

print("=== TOKENIZATION ===")
tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()

print("Tokens:")
for i, token in enumerate(tokens):
    print(f"  {i}: {token.type} -> '{token.value}' (pos: {token.start}-{token.end})")

print()
print("=== PARSING ===")
try:
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print(f"AST: {ast}")
except EnzoParseError as e:
    print("❌ Parse error:")
    print(f"Error: {e}")
    if hasattr(e, 'token'):
        print(f"Error token: {e.token}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
