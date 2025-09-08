import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

print("=== Environment object test ===")
print(f"Environment object ID: {id(_env)}")
print(f"Environment contents before: {list(_env.keys())}")

# Try the same sequence as enzo_fresh
_env.clear()
_initialize_builtin_variants()

print(f"Environment contents after clear+init: {list(_env.keys())}")

# Now define a variable
test_code = '$score: 95;'
ast = parse(test_code)
result = eval_ast(ast)
print(f"Environment contents after $score: {list(_env.keys())}")

# Try to redefine
try:
    ast2 = parse(test_code)
    result2 = eval_ast(ast2)
    print(f"Redefinition successful: {result2}")
except Exception as e:
    print(f"Redefinition failed: {e}")

# Now try the full clear and retry
_env.clear()
_initialize_builtin_variants()
print(f"Environment contents after second clear: {list(_env.keys())}")

try:
    ast3 = parse(test_code)
    result3 = eval_ast(ast3)
    print(f"After clearing, redefinition successful: {result3}")
except Exception as e:
    print(f"After clearing, redefinition failed: {e}")
