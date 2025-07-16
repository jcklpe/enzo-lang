#!/usr/bin/env python3

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

code = '''
[$inner12, $z12] :> $outer12[];
'''

print("=== DEBUGGING RESTRUCTURING SYNTAX ===")
print(f"Code: {code.strip()}")

# Parse and execute
tokenizer = Tokenizer(code)
parser = Parser(code)
statements = parser.parse()

print("\n=== AST ANALYSIS ===")
for i, stmt in enumerate(statements):
    print(f"Statement {i}: {type(stmt).__name__}")
    if hasattr(stmt, 'target_vars'):
        print(f"  target_vars: {stmt.target_vars}")
    if hasattr(stmt, 'source_expr'):
        print(f"  source_expr: {stmt.source_expr}")
    if hasattr(stmt, 'new_var'):
        print(f"  new_var: {getattr(stmt, 'new_var', 'None')}")
    if hasattr(stmt, 'renamed_pairs'):
        print(f"  renamed_pairs: {getattr(stmt, 'renamed_pairs', 'None')}")

env = {'$inner12': 'test_inner', '$z12': 'test_z', '$outer12': 'test_outer'}
print("\n=== EXECUTION ===")
try:
    for i, stmt in enumerate(statements):
        print(f"\nExecuting statement {i}: {type(stmt).__name__}")
        result_value = eval_ast(stmt, env=env)
        if result_value is not None:
            print(f"  Result: {result_value}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
