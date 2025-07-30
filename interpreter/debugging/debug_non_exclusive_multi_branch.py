#!/usr/bin/env python3

# Debug non-exclusive multi-branch evaluation

import sys
sys.path.append('/Users/aslan/work/enzo-lang/interpreter/src')

from enzo_parser.parser import Parser
from evaluator import eval_ast

# Test the specific multi-branch case
test_code = """
$multi-branch-num1: 10;

If $multi-branch-num1 is at least 5,
  "At least 5 matched"; // should print
or is Number,
  "generic number should print"; // should print
end;
"""

parser = Parser(test_code)
try:
    ast = parser.parse()
    print("AST parsing successful")
    print(f"AST: {ast}")

    # Find the If statement
    if_stmt = None
    for stmt in ast:  # AST is a list, not an object with .statements
        if hasattr(stmt, '__class__') and 'IfStatement' in str(stmt.__class__):
            if_stmt = stmt
            break

    if if_stmt:
        print(f"If statement found: {if_stmt}")
        print(f"Has non-exclusive attr: {hasattr(if_stmt, 'is_non_exclusive_multi_branch')}")
        if hasattr(if_stmt, 'is_non_exclusive_multi_branch'):
            print(f"is_non_exclusive_multi_branch: {if_stmt.is_non_exclusive_multi_branch}")
        if hasattr(if_stmt, 'all_branches'):
            print(f"all_branches: {if_stmt.all_branches}")
            print(f"Number of branches: {len(if_stmt.all_branches)}")

    # Evaluating the AST
    print("\nEvaluating...")
    from src.enzo_parser.ast_nodes import Program
    program = Program(ast)
    result = eval_ast(program)
    print(f"Result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
