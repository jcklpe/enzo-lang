#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

def debug_multi_iteration_scope():
    # Reset environment
    _env.clear()

    print("=== Testing Multi-Iteration Fresh Shadow Scope ===")

    # Test the exact case from the failing test
    code = '''
$loop-iteration1: 0;
$local-var: 5;
$local-var;
Loop, (
    $local-var: 1;
    $local-var;
    $local-var + 1 :> $local-var;
    $local-var;
    $loop-iteration1 + 1 :> $loop-iteration1;
    $loop-iteration1;
   If $loop-iteration1 is at least 3, (end-loop);
);
$local-var;
'''

    try:
        print("Parsing and evaluating...")
        ast = parse(code)
        result = eval_ast(ast)

        print(f"Final result: {result}")
        print(f"Final _env state:")
        print(f"  $local-var = {_env.get('$local-var', 'NOT_FOUND')}")
        print(f"  $loop-iteration1 = {_env.get('$loop-iteration1', 'NOT_FOUND')}")

        print(f"\nExpected final $local-var: 5")
        print(f"Actual final $local-var: {_env.get('$local-var', 'NOT_FOUND')}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_multi_iteration_scope()
