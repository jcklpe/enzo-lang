#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.tokenizer import Tokenizer

print("=== TESTING BLOCK COMMENT TOKENIZATION ===")

# Test case 1: Simple multiline block comment
test_code1 = '''$z: 3;
/'
  // The following line should be ignored:
  $z <: 99;
'/
$z;'''

print("Test 1 - Multiline block comment:")
print(repr(test_code1))
print()

try:
    tokenizer = Tokenizer(test_code1)
    tokens = tokenizer.tokenize()
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    print("SUCCESS: Tokenization completed")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50 + "\n")

# Test case 2: Inline block comment
test_code2 = '''$a: 4 /' this part is ignored '/;'''

print("Test 2 - Inline block comment:")
print(repr(test_code2))
print()

try:
    tokenizer = Tokenizer(test_code2)
    tokens = tokenizer.tokenize()
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    print("SUCCESS: Tokenization completed")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
