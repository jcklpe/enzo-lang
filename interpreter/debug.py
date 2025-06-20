#!/usr/bin/env python3
from src.parser import parse
from src.evaluator import eval_ast

# Test 2: simple bind
code = "$y: (10 + 5); $y;"
tree = parse(code)
print("BIND AST:", tree)
eval_ast(tree)