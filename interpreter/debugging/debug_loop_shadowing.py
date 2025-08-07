#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

def debug_loop_shadowing():
    # Test basic loop behavior vs while loop behavior

    print("=== BASIC LOOP TEST ===")
    basic_test = '''
    $x: 0;
    $x;
    Loop, (
        $x: 10;  // shadow
        $x;      // should print 10
        end-loop;
    );
    $x;  // should print 0
    '''

    try:
        parser = Parser(basic_test)
        ast = parser.parse()
        result = eval_ast(ast)
        print('Basic loop result:', result)
    except Exception as e:
        print('Basic loop error:', e)
        import traceback
        traceback.print_exc()

    print("\n=== WHILE LOOP TEST ===")
    while_test = '''
    $x: 0;
    $y: 0;
    $x;
    $y;
    Loop while $y is less than 1, (
        $x: 10;  // shadow
        $x;      // should print 10
        $y + 1 :> $y;  // rebind outer variable - this will exit loop
    );
    $x;  // should print 0 (shadow discarded)
    $y;  // should print 1 (rebinding worked)
    '''

    try:
        parser = Parser(while_test)
        ast = parser.parse()
        result = eval_ast(ast)
        print('While loop result:', result)
    except Exception as e:
        print('While loop error:', e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_loop_shadowing()
