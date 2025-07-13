#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def test_variant_access():
    # Test simple variant access
    test_code = """
    Magic-Type variants: Fire, or Ice, or Wind;
    Magic-Type.Fire;
    """

    print("Testing variant access...")
    print(f"Code: {test_code.strip()}")

    try:
        ast = parse(test_code)
        print(f"AST: {ast}")

        # Evaluate
        result = None
        for stmt in ast:
            result = eval_ast(stmt)

        print(f"Result: {result}")
        print(f"Result type: {type(result)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_variant_access()
