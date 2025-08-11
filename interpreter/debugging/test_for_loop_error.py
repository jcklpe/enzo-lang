#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the for loop error case
test_code = """
Loop for $item10 in 10, (
    $item10;
);
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
