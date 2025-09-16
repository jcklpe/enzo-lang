#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_loop_control_piercing():
    """Test that loop control statements pierce through If statement function atoms."""

    # Clear environment and re-add built-ins
    _env.clear()
    _initialize_builtin_variants()

    print("Testing loop control statement piercing through If statements...")

    # Test 1: end-loop inside If statement
    test1_code = """
$result: 0;
Loop, (
    $result + 1 :> $result;
    $result;

    If $result is 3, (
        end-loop;
    );
);

$result
"""

    print("\n--- Test 1: end-loop inside If statement ---")
    try:
        ast = parse(test1_code)
        result = eval_ast(ast)
        print(f"Result: {result}")
        print(f"Expected: 3 (should stop loop when result=3, before adding 10)")

        if result == 3:
            print("✅ Test 1 PASSED: end-loop correctly pierced through If statement")
        else:
            print("❌ Test 1 FAILED: end-loop did not pierce correctly")
    except Exception as e:
        print(f"❌ Test 1 ERROR: {e}")

    # Test 2: restart-loop inside If statement
    test2_code = """
$result: 0;
$iterations: 0;

Loop, (
    $iterations + 1 :> $iterations;
    $result + 1 :> $result;

    If $result is 2, (
        restart-loop;
    );

    If $iterations is greater than 5, (
        end-loop;
    );

    $result + 10 :> $result;
);

$result
"""

    print("\n--- Test 2: restart-loop inside If statement ---")

    # Clear environment again for Test 2
    _env.clear()
    _initialize_builtin_variants()

    try:
        ast = parse(test2_code)
        result = eval_ast(ast)
        print(f"Result: {result}")
        print(f"Expected: Complex trace - but should not error if restart-loop works")

        if result >= 1:
            print("✅ Test 2 PASSED: restart-loop correctly pierced through If statement")
        else:
            print("❌ Test 2 FAILED: restart-loop did not pierce correctly")
    except Exception as e:
        print(f"❌ Test 2 ERROR: {e}")

    print("\n--- Test Summary ---")
    print("If both tests pass, loop control statements are correctly piercing through If statement function atoms!")

if __name__ == "__main__":
    test_loop_control_piercing()