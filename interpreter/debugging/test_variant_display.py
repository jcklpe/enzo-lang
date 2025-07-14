#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def test_variant_group_display():
    """Test that variant groups display just their name"""

    test_code = '''
True variants: Blahblahblahdoesntmatter;
$signal: True;
$signal;
'''

    print("Testing variant group display...")
    print(f"Code: {test_code.strip()}")
    print()

    try:
        ast = parse(test_code)
        print(f"Parsed {len(ast)} statements:")

        for i, stmt in enumerate(ast):
            print(f"  {i+1}: {type(stmt).__name__}")

        print("\nEvaluating:")
        result = None
        for i, stmt in enumerate(ast):
            result = eval_ast(stmt)
            if result is not None:
                print(f"  Statement {i+1} result: {result}")
                print(f"  Type: {type(result)}")

        print(f"\nFinal result: {result}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_variant_group_display()
