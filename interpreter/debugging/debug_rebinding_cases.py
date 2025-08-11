#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

def debug_rebinding_issue():
    # Reset environment
    _env.clear()

    print("=== Debugging Rebinding Issue ===")

    # Test case 1: Simple rebinding without shadow (should work)
    code1 = """
$temp: 0;
$temp;
Loop, (
    $temp<: 11;
    $temp;
    end-loop;
);
$temp;
"""

    print("Test 1: Simple rebinding (no shadow)")
    try:
        ast1 = parse(code1)
        result1 = eval_ast(ast1)
        print(f"Result: {result1}, Final env: {_env.get('$temp', 'NOT_FOUND')}")
    except Exception as e:
        print(f"Error: {e}")

    # Reset
    _env.clear()

    # Test case 2: Rebinding with prior shadow (complex case)
    code2 = """
$temp: 5;
$temp;
Loop, (
    $temp: 1;
    $temp;
    $temp + 10 :> $temp;
    $temp;
    end-loop;
);
$temp;
"""

    print("\nTest 2: Rebinding shadowed variable")
    try:
        ast2 = parse(code2)
        result2 = eval_ast(ast2)
        print(f"Result: {result2}, Final env: {_env.get('$temp', 'NOT_FOUND')}")
        print("Expected: Result should end with 5 (outer unchanged), Final env: 5")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_rebinding_issue()
