#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

def test_comparison():
    print("=== TESTING BASIC LOOP ===")
    basic_test = '''
    $x: 0;
    Loop, (
        $x: 10;
        end-loop;
    );
    '''

    try:
        parser = Parser(basic_test)
        ast = parser.parse()
        result = eval_ast(ast)
        print('Basic loop succeeded')
    except Exception as e:
        print('Basic loop failed:', e)

    print("\n=== TESTING WHILE LOOP ===")
    while_test = '''
    $x: 0;
    Loop while $x is 0, (
        $x: 10;
    );
    '''

    try:
        parser = Parser(while_test)
        ast = parser.parse()
        result = eval_ast(ast)
        print('While loop succeeded')
    except Exception as e:
        print('While loop failed:', e)
        print('Error type:', type(e))

if __name__ == "__main__":
    test_comparison()
