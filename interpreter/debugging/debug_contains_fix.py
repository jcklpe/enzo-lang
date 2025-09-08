import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

# Test contains on non-List should return False instead of erroring
test_code = '''
$non-list-val: "hello";
If $non-list-val contains 1, (
    "Won't print";
), Else, (
    "Will print";
);
'''

print("=== Testing contains on non-List ===")
print(f"Code: {test_code}")

try:
    ast = parse(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
