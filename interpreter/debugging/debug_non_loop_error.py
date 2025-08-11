#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

def test_non_loop_error():
    # Reset environment
    _env.clear()

    print("=== Testing Non-Loop Error Cases ===")

    # Test case 1: end-loop in function atom
    code1 = '''
(
    "this function atom is not a loop";
    end-loop;
);
'''

    print("Test 1: end-loop in function atom")
    try:
        ast1 = parse(code1)
        result1 = eval_ast(ast1)
        print(f"Result: {result1}")
        print("ERROR: Should have thrown an exception!")
    except Exception as e:
        print(f"Exception (expected): {e}")

    # Test case 2: restart-loop in function atom
    code2 = '''
(
    "this function atom is not a loop";
    restart-loop;
);
'''

    print("\nTest 2: restart-loop in function atom")
    try:
        ast2 = parse(code2)
        result2 = eval_ast(ast2)
        print(f"Result: {result2}")
        print("ERROR: Should have thrown an exception!")
    except Exception as e:
        print(f"Exception (expected): {e}")

if __name__ == "__main__":
    test_non_loop_error()
