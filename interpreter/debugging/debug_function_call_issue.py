import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

code = """
function: (
  param $x: 5;
  return($x + 5);
);

function(5);
"""

print("Parsing and evaluating:")
print(code)
print("=" * 50)

try:
    ast = parse(code)
    print("AST parsed successfully")
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
