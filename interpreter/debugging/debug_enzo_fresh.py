import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

print("=== Testing enzo_fresh behavior ===")

# First run - define $score
print("\n1. First run:")
_env.clear()
_initialize_builtin_variants()
code1 = '$score: 95; $score;'
try:
    ast1 = parse(code1)
    result1 = eval_ast(ast1, value_demand=True)
    print(f"Result: {result1}")
    print(f"Environment after first run: {list(_env.keys())}")
except Exception as e:
    print(f"Error: {e}")

# Second run - redefine $score (should work with fresh environment)
print("\n2. Second run with fresh environment:")
_env.clear()
_initialize_builtin_variants()
code2 = '$score: 100; $score;'
try:
    ast2 = parse(code2)
    result2 = eval_ast(ast2, value_demand=True)
    print(f"Result: {result2}")
    print(f"Environment after second run: {list(_env.keys())}")
except Exception as e:
    print(f"Error: {e}")

# Third run - redefine $score WITHOUT clearing (should error)
print("\n3. Third run WITHOUT clearing environment:")
code3 = '$score: 200; $score;'
try:
    ast3 = parse(code3)
    result3 = eval_ast(ast3, value_demand=True)
    print(f"Result: {result3}")
except Exception as e:
    print(f"Error: {e}")
