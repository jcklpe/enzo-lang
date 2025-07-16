#!/usr/bin/env python3

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

code = '''
$person17: [$age17: 5, $color17: "green"];
$person17[] :> $age17, $color17 -> $fav-color17;
$fav-color17;
'''

print("=== DEBUGGING REVERSE DESTRUCTURING WITH RENAMING ===")
print(f"Code: {code.strip()}")

# Parse
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
    if hasattr(stmt, 'renamed_pairs'):
        print(f"  renamed_pairs: {getattr(stmt, 'renamed_pairs', 'None')}")

# Execute
env = {}
print("\n=== EXECUTION ===")
try:
    for i, stmt in enumerate(statements):
        print(f"\nExecuting statement {i}: {type(stmt).__name__}")
        result_value = eval_ast(stmt, env=env)
        if result_value is not None:
            print(f"  Result: {result_value}")

        # Show environment after each statement
        print(f"  Environment after: {dict(env)}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== FINAL CHECK ===")
print(f"$age17 = {env.get('$age17', 'NOT FOUND')}")
print(f"$fav-color17 = {env.get('$fav-color17', 'NOT FOUND')}")
print(f"$color17 = {env.get('$color17', 'NOT FOUND')}")
