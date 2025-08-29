#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment
_env.clear()

# Test how eval_ast handles multiple statements when one errors
test_code = '''$level-scope: 1;
If $level-scope is 0, (
    $msg-scope: "Level 0";
), Else if $level-scope is 1, (
    $msg-scope: "Level 1";
    "In Else If: <$msg-scope>";
), Else, (
    $msg-scope: "Other Level";
);
$msg-scope;
'''

print("=== Testing eval_ast with multi-statement program ===")
try:
    ast = parse_program(test_code)
    print(f"AST type: {type(ast)}")
    if hasattr(ast, 'statements'):
        print(f"Number of statements: {len(ast.statements)}")
        for i, stmt in enumerate(ast.statements):
            print(f"  Statement {i}: {type(stmt)}")

    print("\nEvaluating...")
    result = eval_ast(ast, value_demand=True)
    print(f"Result: {result}")
    print(f"Result type: {type(result)}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Also test statement by statement
print("\n=== Testing statement by statement ===")
_env.clear()

try:
    ast = parse_program(test_code)
    if hasattr(ast, 'statements'):
        for i, stmt in enumerate(ast.statements):
            print(f"\nEvaluating statement {i}: {type(stmt)}")
            try:
                result = eval_ast(stmt, value_demand=True)
                print(f"  Result: {result}")
                if result is not None:
                    print(f"  Would print: {result}")
            except Exception as e:
                print(f"  Error: {e}")
                break

except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()
