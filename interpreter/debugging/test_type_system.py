#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Environment contents ===")
for key, value in _env.items():
    print(f"{key}: {value} ({type(value)})")

print("\n=== Testing what 'Function' evaluates to ===")
try:
    result = eval_ast(parse('Function;'))
    print(f"'Function' evaluates to: {result} ({type(result)})")
except Exception as e:
    print(f"Error evaluating 'Function': {e}")

print("\n=== Testing function type ===")
try:
    ast = parse('$anon_ref: @(param $x: ; return($x + 1));')
    eval_ast(ast)

    func_obj = _env['$anon_ref']
    print(f"Function object: {func_obj} ({type(func_obj)})")

    # Check what happens in type comparison manually
    result = eval_ast(parse('$anon_ref;'), value_demand=False)
    print(f"$anon_ref with value_demand=False: {result} ({type(result)})")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing simple type comparison ===")
try:
    _env.clear()
    _initialize_builtin_variants()

    # Test with a number first
    eval_ast(parse('$num: 42;'))
    result = eval_ast(parse('$num is Number;'))
    print(f"$num is Number: {result}")

    # Test with text
    eval_ast(parse('$text: "hello";'))
    result = eval_ast(parse('$text is Text;'))
    print(f"$text is Text: {result}")

except Exception as e:
    print(f"Error in simple comparison: {e}")
    import traceback
    traceback.print_exc()
