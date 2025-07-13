#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse

def debug_empty_bind():
    # Test the exact failing case from the regression
    test_code = "$x: ;"

    print(f"Testing: {repr(test_code)}")

    try:
        ast = parse(test_code)
        print(f"✅ Parsed successfully: {ast[0]}")
        print(f"AST type: {type(ast[0]).__name__}")
        if hasattr(ast[0], 'value'):
            print(f"Value: {ast[0].value}")

    except Exception as e:
        print(f"❌ Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_empty_bind()
