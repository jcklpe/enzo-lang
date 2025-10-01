#!/usr/bin/env python3
"""Debug why the second rebind doesn't work."""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Simplest possible test
test = '''
$flag: True;
If $flag, (
    False :> $flag;
);
$flag;
'''

print("=== Testing simple boolean rebind in If ===")
print(f"Code:\n{test}")
print("---")

ast = parse(test)
result = eval_ast(ast)
print(f"Result: {result} (should be False)")
print(f"$flag in env: {_env.get('$flag', 'NOT_FOUND')}")
print(f"flag in env: {_env.get('flag', 'NOT_FOUND')}")