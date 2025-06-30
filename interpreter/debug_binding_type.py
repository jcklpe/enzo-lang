#!/usr/bin/env python3

import sys
sys.path.append('src')

from enzo_parser.parser import parse
from src.enzo_parser.ast_nodes import Binding  # Use same import path as evaluator
from evaluator import eval_ast

def debug_binding():
    code = "times2: (2 * 2); times2();"
    print(f"Testing: {code}")

    ast = parse(code)
    print(f"AST: {ast}")

    # First, let's evaluate the binding
    env = {}
    binding_ast = [ast[0]]  # Just the binding statement
    print("\n--- Evaluating binding ---")
    try:
        result = eval_ast(binding_ast, value_demand=True, env=env)
        print(f"Binding result: {result}")
        print(f"Environment after binding: {env}")

        # Check what type times2 is
        if 'times2' in env:
            times2_val = env['times2']
            print(f"times2 type: {type(times2_val)}")
            print(f"times2 value: {times2_val}")
            from evaluator import EnzoFunction
            print(f"Is EnzoFunction? {isinstance(times2_val, EnzoFunction)}")

    except Exception as e:
        print(f"Binding error: {e}")
        import traceback
        traceback.print_exc()

    # Now test the function call
    print("\n--- Testing function call ---")
    call_ast = [ast[1]]  # Just the function call
    try:
        result = eval_ast(call_ast, value_demand=True, env=env)
        print(f"Call result: {result}")
    except Exception as e:
        print(f"Call error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_binding()