import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse
from src.enzo_parser.ast_nodes import *

# Clear and reinitialize environment
_env.clear()
_initialize_builtin_variants()

# Test the specific failing case
test_code = '''
$inline-test: "inner"
$result-scope: If True, ( $inline-test: "inner"; $inline-test )
'''

print("=== Parsing Test Code ===")
ast = parse(test_code)

print("\n=== AST Structure ===")
# Parse returns a list of statements, not a Program object
statements = ast if isinstance(ast, list) else ast.statements
for i, statement in enumerate(statements):
    print(f"Statement {i}: {type(statement).__name__}")
    if isinstance(statement, Binding):
        print(f"  Variable: {statement.name}")
        print(f"  Value type: {type(statement.value).__name__}")
        if isinstance(statement.value, IfStatement):
            print(f"    Then block length: {len(statement.value.then_block)}")
            for j, then_stmt in enumerate(statement.value.then_block):
                print(f"      Then statement {j}: {type(then_stmt).__name__}")
                if hasattr(then_stmt, 'code_line'):
                    print(f"        Code line: {then_stmt.code_line}")
            if hasattr(statement.value, 'code_line'):
                print(f"    If code line: {statement.value.code_line}")

print("\n=== Evaluating ===")
try:
    # Evaluate the parsed statements
    result = None
    for statement in statements:
        result = eval_ast(statement)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Final Environment ===")
for key, value in _env.items():
    if not key.startswith('_'):
        print(f"{key}: {value}")