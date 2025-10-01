#!/usr/bin/env python3
"""Trace where duplicate keys are created."""

import sys
sys.path.append('..')

# Patch the environment to log all assignments
original_setitem = dict.__setitem__

def traced_setitem(self, key, value):
    if 'flag' in str(key).lower():
        import traceback
        print(f"\n=== Setting env[{key!r}] = {value!r} ===")
        traceback.print_stack(limit=8)
    original_setitem(self, key, value)

dict.__setitem__ = traced_setitem

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
$flag: True;
If $flag, (
    False :> $flag;
);
$flag;
'''

print("=== Parsing and evaluating ===")
ast = parse(test_code)
result = eval_ast(ast)
print(f"\n=== Final result: {result} ===")
print(f"Keys in _env containing 'flag': {[k for k in _env.keys() if 'flag' in str(k).lower()]}")