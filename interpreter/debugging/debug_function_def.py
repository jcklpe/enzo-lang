#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env, _initialize_builtin_variants

# Reset environment
_env.clear()
_initialize_builtin_variants()

code = """function: (param $x: 5; return($x + 5););"""

print("=== Parsing function definition ===")
print(code)
print()

ast = parse(code)
print("AST:")
print(ast)
print()

print("=== Evaluating function definition ===")
result = eval_ast(ast)
print(f"Result: {result}")
print()

print("=== Checking what's in environment ===")
if 'function' in _env:
    func = _env['function']
    print(f"Function object: {func}")
    print(f"Function type: {type(func)}")
    if hasattr(func, 'params'):
        print(f"Function params: {func.params}")
    if hasattr(func, 'param_names'):
        print(f"Function param_names: {func.param_names}")
    if hasattr(func, 'body'):
        print(f"Function body: {func.body}")
print()

print("=== Now trying to call function(5) ===")
call_code = "function(5);"
call_ast = parse(call_code)
print(f"Call AST: {call_ast}")

try:
    call_result = eval_ast(call_ast)
    print(f"Call result: {call_result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
