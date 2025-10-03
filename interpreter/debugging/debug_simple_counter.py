import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Clear and reinitialize environment
_env.clear()
_initialize_builtin_variants()

# Test basic rebinding outside of loops
test_code = '''
$counter: 0;
"Initial counter: <$counter>";
$counter + 1 :> $counter;
"After first rebind: <$counter>";
$counter + 1 :> $counter;
"After second rebind: <$counter>";
$counter;
'''

print("=== Test: Basic rebinding outside loops ===")
ast = parse(test_code)
statements = ast if isinstance(ast, list) else ast.statements

for statement in statements:
    result = eval_ast(statement)

print(f"Final $counter: {_env.get('$counter', 'NOT_FOUND')}")
print(f"Should be: 2")