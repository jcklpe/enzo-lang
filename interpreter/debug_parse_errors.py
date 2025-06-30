#!/usr/bin/env python3

import sys
sys.path.append('src')

from enzo_parser.parser import parse
from evaluator import eval_ast
from error_handling import EnzoParseError

def test_parse_errors():
    test_cases = [
        "(1 + 2",      # missing closing paren
        "(3 + 4;",     # missing closing paren, has semicolon
        "[1, 2, 3",    # missing closing bracket
        "{ $a: 1, $b: 2"  # missing closing brace
    ]

    for i, case in enumerate(test_cases):
        print(f"\n=== Test case {i+1}: {repr(case)} ===")
        try:
            ast = parse(case)
            print(f"Parse successful: {ast}")
            try:
                result = eval_ast(ast, value_demand=True)
                print(f"Eval result: {result}")
            except Exception as e:
                print(f"Eval error: {e}")
        except EnzoParseError as e:
            print(f"Parse error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_parse_errors()
