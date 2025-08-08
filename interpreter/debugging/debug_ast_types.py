#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

def debug_binding_vs_rebinding():
    # Reset environment
    _env.clear()

    print("=== Testing Binding vs Rebinding Distinction ===")

    # Test what AST nodes are created
    code1 = "$temp: 5;"  # Should be Binding
    code2 = "$temp<: 10;"  # Should be BindOrRebind

    ast1 = parse(code1)
    ast2 = parse(code2)

    print(f"Code1 AST: {ast1}")
    print(f"Code2 AST: {ast2}")

    if hasattr(ast1, 'statements'):
        print(f"Statement 1 type: {type(ast1.statements[0])}")
    else:
        print(f"Statement 1 (direct): {type(ast1)}")

    if hasattr(ast2, 'statements'):
        print(f"Statement 2 type: {type(ast2.statements[0])}")
    else:
        print(f"Statement 2 (direct): {type(ast2)}")

if __name__ == "__main__":
    debug_binding_vs_rebinding()
