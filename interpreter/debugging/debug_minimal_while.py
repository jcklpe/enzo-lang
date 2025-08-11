#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

def test_simple_while_shadowing():
    test_code = '''
    $x: 0;
    Loop while $x is less than 1, (
        $x: 10;
    );
    '''

    try:
        parser = Parser(test_code)
        ast = parser.parse()
        result = eval_ast(ast)
        print('Result:', result)
    except Exception as e:
        print('Error:', e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_while_shadowing()
