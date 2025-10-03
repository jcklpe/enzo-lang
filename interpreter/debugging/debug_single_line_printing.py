import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Clear and reinitialize environment
_env.clear()
_initialize_builtin_variants()

# Test the specific failing case
test_code = '''
If True, ("passing one statement from inline If"; "passing a second one");
'''

print("=== Testing single-line function atom behavior ===")
print("Code:", repr(test_code.strip()))

print("\n=== Evaluating ===")
try:
    ast = parse(test_code)
    for statement in ast:
        result = eval_ast(statement)
        print(f"Statement result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()