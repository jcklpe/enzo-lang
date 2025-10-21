import sys
import traceback
sys.path.append('..')

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env, _initialize_builtin_variants

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = """
$original-ref: [1, 2, 3];

modify-reference: (
    param $list: ;
    $list.1 <: 99;
    $list;
);

modify-reference(@original-ref);
$original-ref;
"""

try:
    ast = parse(test_code)
    print("AST parsed successfully")
    print("=" * 50)

    result = eval_ast(ast)
    print("Result:", result)
except Exception as e:
    print("=" * 50)
    print("ERROR OCCURRED:")
    print(type(e).__name__, ":", str(e))
    print("=" * 50)
    print("FULL TRACEBACK:")
    traceback.print_exc()
    print("=" * 50)
