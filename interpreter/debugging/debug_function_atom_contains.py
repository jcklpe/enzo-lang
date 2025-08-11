#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import Parser

# Test just the function atom part
test_code = """($this contains 4)"""

print("=== TEST CODE ===")
print(repr(test_code))
print("\n=== PARSING ===")

try:
    parser = Parser(test_code)
    # Manually set the pipeline flag to simulate being in a pipeline context
    parser.in_pipeline_function = True
    result = parser.parse_statement()
    print("SUCCESS:", result)
except Exception as e:
    print("ERROR:", e)
    print("ERROR TYPE:", type(e).__name__)
