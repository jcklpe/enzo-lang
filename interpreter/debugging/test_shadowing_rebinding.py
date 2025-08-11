#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

def test_loop_shadowing_rebinding():
    # Test the "Loop function atom shadowing" case
    code = '''
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
        # Reset environment for clean testing
        _env.clear()

        print("Testing loop shadowing vs rebinding...")

        # Parse and evaluate
        ast = parse(code)
        result = eval_ast(ast)

        print(f"Final result: {result}")
        print("Expected pattern: [0, 10, 0, 11, 11]")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_loop_shadowing_rebinding()
