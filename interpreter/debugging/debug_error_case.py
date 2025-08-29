#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = """
anon_ref_apply: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);

anon_ref_apply( (param $x:; $x * 2), 5 );
"""

print("=== TESTING ERROR CASE ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Unexpected success: {result}")
except Exception as e:
    print(f"ERROR (as expected): {e}")
    print(f"Error type: {type(e).__name__}")
