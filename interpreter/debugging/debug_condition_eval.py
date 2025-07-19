#!/usr/bin/env python3

import sys
sys.path.append('src')

from src.evaluator import eval_ast
from src.enzo_parser.parser import Parser

def debug_condition_evaluation():
    code = '''$status-if: "ready";

If $status-if,
  "Ready!";
end;'''

    print("=== DEBUGGING CONDITION EVALUATION ===")

    # Parse
    parser = Parser(code)
    ast = parser.parse()

    print(f"AST: {ast}")

    # Get the If statement
    if_stmt = ast[1]  # Second statement
    print(f"If statement: {if_stmt}")
    print(f"Condition: {if_stmt.condition}")
    print(f"Condition type: {type(if_stmt.condition)}")

    # Set up environment
    env = {}

    # Evaluate first statement (binding)
    binding_result = eval_ast(ast[0], env=env)
    print(f"After binding, env: {env}")

    # Evaluate condition separately
    print(f"\n=== EVALUATING CONDITION ===")
    condition_result = eval_ast(if_stmt.condition, env=env)
    print(f"Condition result: {condition_result}")
    print(f"Condition result type: {type(condition_result)}")

    # Test truthiness
    from src.evaluator import _is_truthy
    is_truthy = _is_truthy(condition_result)
    print(f"Is truthy: {is_truthy}")

    # Evaluate full If statement
    print(f"\n=== EVALUATING IF STATEMENT ===")
    if_result = eval_ast(if_stmt, env=env)
    print(f"If statement result: {if_result}")

if __name__ == "__main__":
    debug_condition_evaluation()
