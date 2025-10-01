import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Clear and reinitialize environment
_env.clear()
_initialize_builtin_variants()

# Test loop variable accumulation
test_code = '''
$counter: 0;
$counter;
Loop, (
    $counter + 1 :> $counter;
    $counter;
    If $counter is 3, (end-loop;);
);
$counter;
'''

print("=== Test: Loop variable accumulation ===")
ast = parse(test_code)
statements = ast if isinstance(ast, list) else ast.statements

for statement in statements:
    result = eval_ast(statement)

print(f"Final $counter: {_env.get('$counter', 'NOT_FOUND')}")
print(f"Should be 3")