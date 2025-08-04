#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import Parser

# Test the problematic pipeline case
test_code = """$list-pipe
then ($this contains 4) :> $contains-four;"""

print("=== TEST CODE ===")
print(repr(test_code))
print("\n=== PARSING ===")

try:
    parser = Parser(test_code)
    result = parser.parse_statement()
    print("SUCCESS:", result)
except Exception as e:
    print("ERROR:", e.message if hasattr(e, 'message') else str(e))
    print("ERROR TYPE:", type(e).__name__)
    if hasattr(e, 'code_line'):
        print("CODE LINE:")
        print(e.code_line)
