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
$active-while: True;
$counter-while: 0;
Loop while $active-while and $counter-while is less than 5, (
    $counter-while + 1 :> $counter-while;
    "Counter: <$counter-while>";

    If $counter-while is 5, (
        False :> $active-while;
    );
);
$active-while;
'''

print("=== Before Execution ===")
print("Global environment keys:", list(_env.keys()))

print("\n=== Parsing and Executing ===")
try:
    ast = parse(test_code)
    statements = ast if isinstance(ast, list) else ast.statements

    for statement in statements:
        print(f"\n--- Executing: {type(statement).__name__} ---")
        result = eval_ast(statement)
        print(f"Result: {result}")

        print("Global environment after this statement:")
        for key, value in _env.items():
            if not key.startswith('_'):
                print(f"  {key}: {value}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Final Environment ===")
for key, value in _env.items():
    if not key.startswith('_'):
        print(f"{key}: {value}")