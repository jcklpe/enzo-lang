#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from enzo_parser.ast_nodes import Invoke

def test_function_call_detection():
    # Test different types of statements
    test_cases = [
        "$donald.position.3;",     # property access - should print
        "$donald.fly(5);",         # function call - should not print
        "$x: $donald.fly(5);",     # binding with function call - should not print the call result
    ]

    for test_code in test_cases:
        print(f"\nTesting: {test_code}")
        try:
            ast = parse(test_code)
            stmt = ast[0]
            print(f"AST type: {type(stmt).__name__}")

            # Check if this is a standalone function call
            is_function_call = isinstance(stmt, Invoke)
            print(f"  → Is function call: {is_function_call}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_function_call_detection()
