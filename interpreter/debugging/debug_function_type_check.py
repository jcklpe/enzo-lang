#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== TESTING FUNCTION EVALUATION ===")
test_code = """
$test_func: (param $x:5; $x * 2);
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    func_obj = _env['$test_func']
    print(f"Function object: {func_obj}")
    print(f"Function type: {type(func_obj)}")
    print(f"Is Function? {func_obj.__class__.__name__ == 'EnzoFunction'}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING FUNCTION TYPE CHECKING ===")
test_code2 = """
$test_func: (param $x:5; $x * 2);
If $test_func is Function, ( "It's a Function!" );
"""

try:
    ast = parse(test_code2)
    result = eval_ast(ast)
    print("Type check completed")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== TESTING anon_ref_apply CALL ===")
test_code3 = """
anon_ref_apply: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);

$my_func: (param $x:5; $x * 2);
anon_ref_apply( $my_func, "text" );
"""

try:
    ast = parse(test_code3)
    result = eval_ast(ast)
    print(f"Call succeeded: {result}")
except Exception as e:
    print(f"ERROR: {e}")
