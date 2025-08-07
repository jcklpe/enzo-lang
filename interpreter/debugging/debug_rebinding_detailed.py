#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

def debug_loop_rebinding():
    # Reset environment
    _env.clear()

    print("=== Testing Loop Rebinding Debug ===")

    # Step 1: Set initial value
    code1 = "$loop-temp: 0;"
    ast1 = parse(code1)
    eval_ast(ast1)
    print(f"1. After initial set: _env['$loop-temp'] = {_env.get('$loop-temp', 'NOT_FOUND')}")

    # Step 2: Read initial value
    code2 = "$loop-temp;"
    ast2 = parse(code2)
    result2 = eval_ast(ast2)
    print(f"2. Reading initial: {result2}")

    # Step 3: Loop with shadow
    code3 = """
    Loop, (
        $loop-temp: 10;
        $loop-temp;
        end-loop;
    );
    """
    ast3 = parse(code3)
    result3 = eval_ast(ast3)
    print(f"3. After shadow loop: result={result3}, _env['$loop-temp'] = {_env.get('$loop-temp', 'NOT_FOUND')}")

    # Step 4: Read after shadow
    code4 = "$loop-temp;"
    ast4 = parse(code4)
    result4 = eval_ast(ast4)
    print(f"4. Reading after shadow: {result4}")

    # Step 5: Loop with rebinding
    print("\n=== Testing Rebinding ===")
    code5 = """
    Loop, (
        $loop-temp<: 11;
        $loop-temp;
        end-loop;
    );
    """
    ast5 = parse(code5)
    result5 = eval_ast(ast5)
    print(f"5. After rebind loop: result={result5}, _env['$loop-temp'] = {_env.get('$loop-temp', 'NOT_FOUND')}")

    # Step 6: Final read
    code6 = "$loop-temp;"
    ast6 = parse(code6)
    result6 = eval_ast(ast6)
    print(f"6. Final read: {result6}")

    print(f"\nFull pattern: [0, 10, 0, 11, {result6}]")
    print(f"Expected:     [0, 10, 0, 11, 11]")

if __name__ == "__main__":
    debug_loop_rebinding()
