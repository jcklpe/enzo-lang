#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the exact failing case from the test suite
test_code = """
$list-for-copy2: [10, 20, 30];
Loop for @item in $list-for-copy2, (
  $item <: $item + 1;
  "Item is now <$item>";
);
$list-for-copy2;
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Loop results: {result}")
    print(f"Final list state: {_env.get('$list-for-copy2', 'NOT FOUND')}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
