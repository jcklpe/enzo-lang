#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

def test_current_loop_behavior():
    # Test exactly what the failing test does
    test_code = '''
    $loop-temp: 0;
    $loop-temp;
    Loop, (
        $loop-temp: 10;
        $loop-temp;
        end-loop;
    );
    $loop-temp;
    Loop, (
        $loop-temp<: 11;
        $loop-temp;
        end-loop;
    );
    $loop-temp;
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
    test_current_loop_behavior()
