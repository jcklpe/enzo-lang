#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
$list-of-lists: [[1, 2], ["a", "b"]];
Loop for $inner in $list-of-lists, (
    "Inner List: <$inner>";
    $inner.1;
);
'''

print("=== FOR LOOP LIST OF LISTS DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
