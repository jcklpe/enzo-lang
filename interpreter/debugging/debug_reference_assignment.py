#!/usr/bin/env python3

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

code = '''
$person8: [$name8: "Dana", $age8: 50];
@person8[] :> $n8, $a8;
"Denise" :> $n8;
$person8.name8;
'''

print("=== DEBUGGING REFERENCE DESTRUCTURING ===")
print(f"Code: {code.strip()}")

# Parse and execute
tokenizer = Tokenizer(code)
parser = Parser(code)
statements = parser.parse()

env = {}
print("\n=== EXECUTION ===")
try:
    for i, stmt in enumerate(statements):
        print(f"\nExecuting statement {i}: {type(stmt).__name__}")
        result_value = eval_ast(stmt, env=env)
        if result_value is not None:
            print(f"  Result: {result_value}")

        # Show what $n8 is after reference destructuring
        if '$n8' in env:
            print(f"  $n8 type: {type(env['$n8'])}")
            print(f"  $n8 value: {env['$n8']}")
            if hasattr(env['$n8'], 'reference'):
                print(f"  $n8 reference: {env['$n8'].reference}")
                print(f"  $n8 reference type: {type(env['$n8'].reference)}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
