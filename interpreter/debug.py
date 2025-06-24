#!/usr/bin/env python3
from src.parser import parse
from src.evaluator import eval_ast, _env

def debug_expr(src):
    print("Source:", src)
    ast = parse(src)
    print("AST:", ast)
    try:
        result = eval_ast(ast)
        print("Result:", result)
    except Exception as e:
        print("Exception:", e)

# Try the problematic case(s):
# Case 1: Paren expression as top-level
debug_expr("(10 + 5);")

# Case 2: Arithmetic with bound math functions
_env.clear()
debug_expr("$math1: (10); $math2: (5); ($math1 + $math2);")

# Case 3: String interpolation with paren
_env.clear()
debug_expr('"2 times 2 is <(2*2)>.";')
