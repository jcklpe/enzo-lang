#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def test_parse_bind_issue():
    # Test the problematic line
    test_code = """
    Magic-Type variants: Fire, or Ice;
    $wizard-attacks: [
        $attack-spell-1: Magic-Type.Fire
    ];
    $wizard-attacks.bad-spell: Magic-Type.Plasma;
    """

    print("Testing parsing of binding to list property...")
    print(f"Code: {test_code.strip()}")

    try:
        ast = parse(test_code)
        print(f"AST parsed successfully: {len(ast)} statements")
        for i, stmt in enumerate(ast):
            print(f"  Statement {i}: {type(stmt).__name__}")

        # Try to evaluate
        result = None
        for stmt in ast:
            try:
                result = eval_ast(stmt)
                print(f"Evaluated: {result}")
            except Exception as e:
                print(f"Evaluation error: {e}")

    except Exception as e:
        print(f"Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_parse_bind_issue()
