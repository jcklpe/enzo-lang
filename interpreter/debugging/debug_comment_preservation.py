#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.enzo_parser.parser import Parser

# Test the exact case from lazy-syntax.enzo
test_code_with_comments = "$lazy-var: 0; // error: cannot use `$` in assignment context"
test_code_without_comments = "$lazy-var: 0;"

print("Testing code WITH comments:")
print(f"Input: {repr(test_code_with_comments)}")
try:
    parser = Parser(test_code_with_comments)
    ast = parser.parse()
except Exception as e:
    print(f"Error: {e}")
    print(f"Error code_line: {repr(e.code_line) if hasattr(e, 'code_line') else 'No code_line'}")

print("\nTesting code WITHOUT comments:")
print(f"Input: {repr(test_code_without_comments)}")
try:
    parser = Parser(test_code_without_comments)
    ast = parser.parse()
except Exception as e:
    print(f"Error: {e}")
    print(f"Error code_line: {repr(e.code_line) if hasattr(e, 'code_line') else 'No code_line'}")
