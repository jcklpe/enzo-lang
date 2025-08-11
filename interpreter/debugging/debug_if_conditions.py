#!/usr/bin/env python3

from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast, _is_truthy

# Test the exact failing conditions in If statement context
test_cases = [
    'If [0,0,0], "Won\'t print4"; end;',
    'If False, "Won\'t print5"; end;',
    'If ( ), "Won\'t print1"; end;',
    'If (5 - 5), "Won\'t print2"; end;'
]

print("=== TESTING FAILING CONDITIONS IN IF CONTEXT ===")

for i, code in enumerate(test_cases):
    print(f"\nTest {i+1}: {code}")
    try:
        ast = parse_program(code)
        print(f"  AST: {ast}")

        result = eval_ast(ast, value_demand=True)
        print(f"  Result: {result}")

        if result and len(result) > 0:
            print("  ❌ SHOULD NOT PRINT but did!")
        else:
            print("  ✅ Correctly did not print")

    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
