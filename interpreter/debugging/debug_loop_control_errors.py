#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_loop_control_errors():
    """Test that loop control statements give proper errors inside named functions."""

    # Clear environment and re-add built-ins
    _env.clear()
    _initialize_builtin_variants()

    print("Testing loop control statement error messages...")

    # Test: end-loop inside named function
    test_code = """
$test-func: (
    "this function atom is not a loop";
    end-loop;
);

$test-func
"""

    print("\n--- Testing end-loop inside named function ---")
    try:
        ast = parse(test_code)
        result = eval_ast(ast)
        print(f"❌ ERROR: Should have thrown an error but got: {result}")
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")

        if "error: `end-loop;` inside a non-loop function atom" in error_msg:
            print("✅ PASSED: Correct error message for end-loop in named function")
        else:
            print("❌ FAILED: Wrong error message for end-loop in named function")

if __name__ == "__main__":
    test_loop_control_errors()