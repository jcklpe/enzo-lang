#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("Test 1: Function with default parameter, called with no args")
code1 = """
function: (
  param $x: 5;
  return($x + 5);
);
function();
"""
try:
    ast = parse(code1)
    result = eval_ast(ast)
    print(f"✓ Result: {result}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nTest 2: Function with default parameter, called with one arg")
_env.clear()
_initialize_builtin_variants()

code2 = """
function: (
  param $x: 5;
  return($x + 5);
);
function(10);
"""
try:
    ast = parse(code2)
    result = eval_ast(ast)
    print(f"✓ Result: {result}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nTest 3: Function with required parameter (no default)")
_env.clear()
_initialize_builtin_variants()

code3 = """
function: (
  param $x;
  return($x + 5);
);
function(10);
"""
try:
    ast = parse(code3)
    result = eval_ast(ast)
    print(f"✓ Result: {result}")
except Exception as e:
    print(f"✗ Error: {e}")
