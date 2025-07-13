#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def debug_redefinition():
    test_code = """
    $x: 5;
    $x: 10;
    """

    print("Testing variable redefinition detection...")
    print(f"Code: {test_code.strip()}")

    try:
        ast = parse(test_code)
        print(f"✅ Parsed successfully: {len(ast)} statements")

        # Evaluate
        for i, stmt in enumerate(ast):
            try:
                result = eval_ast(stmt)
                print(f"Statement {i}: {result}")
            except Exception as e:
                print(f"Statement {i} error: {e}")

    except Exception as e:
        print(f"Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_redefinition()
