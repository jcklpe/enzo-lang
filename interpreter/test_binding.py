#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def test_binding():
    # Test the binding behavior
    code = "times2: (2 * 2);"

    print(f'Testing: {code}')

    ast = parse(code)
    print(f'AST: {ast}')

    result = eval_ast(ast, value_demand=True)
    print(f'Result: {result}')
    print(f'Result type: {type(result)}')

if __name__ == "__main__":
    test_binding()
