#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the for loop with @ reference
test_code = """
$list-for-ref: [10, 20, 30];
Loop for @item in $list-for-ref, (
  $item <: $item + 1; // Mutating the original variable
  "Item is now <$item>"; // prints 11, 21, 31
);
$list-for-ref; // should print [11, 21, 31] - original list has changed
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
