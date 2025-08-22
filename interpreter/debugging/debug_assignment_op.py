#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.enzo_parser.tokenizer import Tokenizer

# Test the problematic assignment line
test_code = '$self.count + 1 :> @self.count;'

print(f"Test code: {test_code}")
print()

try:
    # First check tokenization
    tokenizer = Tokenizer(test_code)
    tokens = tokenizer.tokenize()
    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type} -> '{token.value}'")
    print()

    # Then try parsing
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print("AST:", ast)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
