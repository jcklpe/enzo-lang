#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def test_builtin_variants():
    """Test the built-in variant groups"""

    test_cases = [
        # Test built-in True/False variant groups
        "$signal: True; $signal;",
        "$ready: False; $ready;",
        "$status: Status; $status;",

        # Test accessing Status variants
        "$good: Status.True; $good;",
        "$bad: Status.False; $bad;",

        # Test that user can extend Status (this should work now)
        "Status variants: True, or False, or Loading; $loading: Status.Loading; $loading;",

        # Test that extended Status still has original variants
        "Status variants: True, or False, or Loading; $original: Status.True; $original;",
    ]

    for i, test_code in enumerate(test_cases):
        print(f"\n=== Test {i+1}: {test_code} ===")

        try:
            ast = parse(test_code)
            for stmt in ast:
                result = eval_ast(stmt)
                if result is not None:
                    print(f"✅ Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_builtin_variants()
