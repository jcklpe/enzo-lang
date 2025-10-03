#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_if_expression_return():
    """Test that If statements return their computed values when used as expressions."""

    # Clear environment and re-add built-ins
    _env.clear()
    _initialize_builtin_variants()

    print("Testing If statement expression return values...")

    # Test 1: Simple inline If
    test1_code = """
$result: If True, ( "inner" );
$result
"""

    print("\n--- Test 1: Simple If expression ---")
    try:
        ast = parse(test1_code)
        result = eval_ast(ast)
        print(f"Result: {result}")
        print(f"Expected: 'inner'")

        if result == "inner":
            print("✅ Test 1 PASSED: If expression returned correct value")
        else:
            print("❌ Test 1 FAILED: If expression returned wrong value")
    except Exception as e:
        print(f"❌ Test 1 ERROR: {e}")

    # Test 2: Multiline If expression (from failing test)
    test2_code = """
$inline-test: "outer";
$result-scope: If True, ( $inline-test: "inner"; $inline-test ), Else, ( "never" );
$result-scope
"""

    print("\n--- Test 2: Multiline If expression ---")
    # Clear environment again
    _env.clear()
    _initialize_builtin_variants()

    try:
        ast = parse(test2_code)
        result = eval_ast(ast)
        print(f"Result: {result}")
        print(f"Expected: 'inner'")

        if result == "inner":
            print("✅ Test 2 PASSED: Multiline If expression returned correct value")
        else:
            print("❌ Test 2 FAILED: Multiline If expression returned wrong value")
    except Exception as e:
        print(f"❌ Test 2 ERROR: {e}")

if __name__ == "__main__":
    test_if_expression_return()