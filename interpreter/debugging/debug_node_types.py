import sys
sys.path.append('..')
from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env, _initialize_builtin_variants

print("=== Environment Setup ===")
_env.clear()
_initialize_builtin_variants()
print(f"Environment: {list(_env.keys())}")

print("\n=== Testing List Atom ===")
list_code = "[1, 2, 3]"
try:
    list_ast = parse(list_code)
    print(f"Parsed AST: {list_ast}")
    print(f"First node type: {type(list_ast[0])}")
    result = eval_ast(list_ast[0], value_demand=True)
    print(f"Result: {result}")
    print(f"Result type: {type(result)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing Function Atom ===")
func_code = "(param $x: 1; return($x);)"
try:
    func_ast = parse(func_code)
    print(f"Parsed AST: {func_ast}")
    print(f"First node type: {type(func_ast[0])}")
    result = eval_ast(func_ast[0], value_demand=True)
    print(f"Result: {result}")
    print(f"Result type: {type(result)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
