#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env, _initialize_builtin_variants

# Reset environment
_env.clear()
_initialize_builtin_variants()

# Simulate REPL with MULTILINE input (like you're actually typing)
stmt1 = """function: (
param $x: 5;
return($x + 5);
);"""

print(f"=== Multiline Statement 1 ===")
print(stmt1)
print()

ast1 = parse(stmt1)
print(f"AST: {ast1}")
print()

result1 = eval_ast(ast1, value_demand=True)
print(f"Result: {result1}")
print()

# Check environment after definition
print("=== Environment after definition ===")
if 'function' in _env:
    func = _env['function']
    print(f"'function' in environment: {func}")
    if hasattr(func, 'params'):
        print(f"  params: {func.params}")
print()

# Simulate REPL: second statement calls function
stmt2 = "function(5);"
print(f"=== Statement 2: {stmt2} ===")
ast2 = parse(stmt2)
print(f"AST: {ast2}")
try:
    result2 = eval_ast(ast2, value_demand=True)
    print(f"Result: {result2}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
