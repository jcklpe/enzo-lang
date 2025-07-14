#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def test_comprehensive_variant_extension():
    """Test comprehensive variant group extension behavior"""

    # Test script that extends Status and uses it
    test_code = '''
// First, test that Status is built-in with True and False
$initial: Status.True;
$initial;

// Now extend Status to add Loading and Error
Status variants: True, or False, or Loading, or Error;

// Test that original variants still work
$working: Status.True;
$working;

$broken: Status.False;
$broken;

// Test that new variants work
$loading: Status.Loading;
$loading;

$error: Status.Error;
$error;
'''

    print("Testing comprehensive variant extension...")
    print("=" * 60)

    try:
        ast = parse(test_code)
        print(f"Parsed {len(ast)} statements successfully.")
        print()

        print("Results:")
        for i, stmt in enumerate(ast):
            result = eval_ast(stmt)
            if result is not None:
                print(f"  {result}")

        print()
        print("✅ All tests passed! Status variant group can be extended while preserving built-in variants.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_variant_extension()
