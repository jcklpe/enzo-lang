#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast, _env

# Test just the failing blueprint interpolation case
code = '''
BP-example: <[foo: Number]>;
$bp1: BP-example[$foo: 10];
$li31: [<$bp1>];
'''

print("=== TESTING SINGLE CASE ===")
print(f"Code:\n{code}")

try:
    parser = Parser(code)
    ast = parser.parse()
    print(f"\nAST: {ast}")

    # Execute each statement
    for i, stmt in enumerate(ast):
        print(f"\nExecuting statement {i}: {stmt}")
        try:
            result = eval_ast(stmt, env=_env)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Exception: {type(e).__name__}: {e}")
            # Print the error with context like the test runner would
            if hasattr(e, 'code_line') and e.code_line:
                print(f"    {e.code_line}")

except Exception as e:
    print(f"\nException: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
