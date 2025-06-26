#!/usr/bin/env python3
# debug.py -- ephemeral debug script for Enzo parser/tokenizer
from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env

code = '''
$Var123: 10;
$var-xyz: 20;
($Var123 + $var-xyz);
'''

def print_tokens(code):
    print("TOKENS:")
    for t in Tokenizer(code).tokenize():
        print(t)
    print()

def print_ast(code):
    print("AST:")
    ast = parse(code)
    print(ast)
    print()
    return ast

def print_eval(ast):
    print("EVAL:")
    result = eval_ast(ast)
    print(result)
    print()

if __name__ == "__main__":
    print_tokens(code)
    ast = print_ast(code)
    print_eval(ast)
