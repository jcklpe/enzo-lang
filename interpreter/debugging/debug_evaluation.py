#!/usr/bin/env python3

import sys
sys.path.append('src')

from src.enzo_parser.parser import parse_program, parse
from src.evaluator import eval_ast

def debug_evaluation():
    statement = '''If $status-if,
  "Ready!"; // should print "Ready!"
end;'''

    # Set up environment like the first statement would
    env = {"$status-if": "ready", "status-if": "ready"}

    print("=== DEBUGGING EVALUATION ===")
    print(f"Environment: {env}")

    # Test parse_program + eval_ast
    print("\n=== USING parse_program + eval_ast ===")
    try:
        program_ast = parse_program(statement)
        print(f"Program AST: {program_ast}")

        result = eval_ast(program_ast, value_demand=True, env=env)
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

    # Test parse + eval_ast
    print("\n=== USING parse + eval_ast ===")
    try:
        regular_ast = parse(statement)
        print(f"Regular AST: {regular_ast}")

        # For list AST, evaluate each statement
        result = None
        for stmt in regular_ast:
            result = eval_ast(stmt, value_demand=True, env=env)
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_evaluation()
