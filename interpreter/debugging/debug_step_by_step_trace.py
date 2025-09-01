#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== STEP BY STEP DEBUGGING ===")

print("1. Define anon_ref_apply...")
try:
    eval_ast(parse("""
    anon_ref_apply: (
        param $func: ();
        param $value: "";
        return( $func($value) );
    );
    """))
    print("   anon_ref_apply defined successfully")
except Exception as e:
    print(f"   ERROR: {e}")

print("2. Define test function...")
try:
    eval_ast(parse("$my_func: (param $x:5; $x * 2);"))
    print("   $my_func defined successfully")
    print(f"   Type: {type(_env['$my_func'])}")
except Exception as e:
    print(f"   ERROR: {e}")

print("3. Test simple function call...")
try:
    result = eval_ast(parse("$my_func(10);"))
    print(f"   $my_func(10) = {result}")
except Exception as e:
    print(f"   ERROR: {e}")

print("4. Test anon_ref_apply with simple arguments...")
try:
    result = eval_ast(parse('anon_ref_apply( (), "test" );'))
    print(f"   anon_ref_apply( (), \"test\" ) = {result}")
except Exception as e:
    print(f"   ERROR: {e}")

print("5. Test the problematic call...")
try:
    result = eval_ast(parse('anon_ref_apply( $my_func, "text" );'))
    print(f"   anon_ref_apply( $my_func, \"text\" ) = {result}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
