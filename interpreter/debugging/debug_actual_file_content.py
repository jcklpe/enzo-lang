#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

from enzo_parser.parser import Parser
from enzo_parser.tokenizer import Tokenizer

# Test with the actual content from the test file - without leading newline
test_code = '''$list-pipe
then ($this contains 4) :> $contains-four;  // error: comparison word in pipeline'''

print("=== ACTUAL FILE CONTENT TEST ===")
print("Input code:")
print(repr(test_code))

try:
    parser = Parser(test_code)
    print(f"\nTokens: {[(t.type, t.value, t.start, t.end) for t in parser.tokens]}")

    # Try to parse and see where it fails
    parser.parse()
except Exception as e:
    print(f"\nError occurred: {e}")
    print(f"Error type: {type(e).__name__}")

    # If it has a code_line attribute, show it
    if hasattr(e, 'code_line'):
        print(f"\nCode line from error:")
        print(repr(e.code_line))
        print("\nFormatted code line:")
        print(e.code_line)

        # Count leading spaces on each line
        lines = e.code_line.split('\n')
        for i, line in enumerate(lines):
            leading_spaces = len(line) - len(line.lstrip())
            print(f"Line {i}: {leading_spaces} leading spaces: {repr(line)}")
