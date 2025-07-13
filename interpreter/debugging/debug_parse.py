#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def debug_parse_error():
    # Test the problematic line in isolation
    test_code = "$wizard-attacks.bad-spell: Magic-Type.Plasma;"

    print(f"Testing line: {test_code}")

    try:
        ast = parse(test_code)
        print(f"Parsed successfully: {ast}")
        print(f"AST type: {type(ast[0]).__name__}")

    except Exception as e:
        print(f"Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_parse_error()
