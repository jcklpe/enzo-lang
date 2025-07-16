#!/usr/bin/env python3

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

code = '''
$outer12: [ [$x12: 5, $y12: 9], 2 ];
$inner12, $z12: $outer12[];
$inner12.x <: 7;
$inner12.x;
[$inner12, $z12] :> $outer12[];
$outer12.1.x;
'''

print("=== DEBUGGING NESTED RESTRUCTURING ===")
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
        
        # Show key variables after each step
        if '$inner12' in env:
            inner12 = env['$inner12']
            print(f"  $inner12: {inner12}")
            if hasattr(inner12, '_key_map'):
                print(f"  $inner12 keys: {list(inner12._key_map.keys())}")
        
        if '$outer12' in env:
            outer12 = env['$outer12']
            print(f"  $outer12: {outer12}")
            if hasattr(outer12, '_elements') and len(outer12._elements) > 0:
                first_elem = outer12._elements[0]
                print(f"  $outer12[0]: {first_elem}")
                if hasattr(first_elem, '_key_map'):
                    print(f"  $outer12[0] keys: {list(first_elem._key_map.keys())}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
