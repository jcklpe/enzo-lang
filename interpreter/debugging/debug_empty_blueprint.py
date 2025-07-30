#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast, _is_truthy

# Test the exact failing case
code = '''EmptyBP: <[]>;
$empty-bp: EmptyBP[];
$empty-bp;'''

print("=== DEBUGGING EMPTY BLUEPRINT ===")
print(f"Code: {code}")

try:
    parser = Parser(code)
    ast = parser.parse()
    print(f"✅ Parsed successfully: {ast}")

    env = {}
    for i, stmt in enumerate(ast):
        try:
            result = eval_ast(stmt, env=env)
            print(f"Statement {i+1} result: {result} (type: {type(result).__name__})")
            if i == 1:  # The blueprint instantiation
                print(f"  Is truthy: {_is_truthy(result)}")
        except Exception as e:
            print(f"❌ Evaluation error: {e}")
            import traceback
            traceback.print_exc()
            break

except Exception as e:
    print(f"❌ Parse error: {e}")
    import traceback
    traceback.print_exc()
