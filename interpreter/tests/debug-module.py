# tests/debug-module.py

from src.parser import parse
from src.evaluator import eval_ast
import traceback

def debug_case(source):
    print("=" * 60)
    print(f"Source: {source}")
    try:
        ast = parse(source)
        print("AST:", ast)
        try:
            result = eval_ast(ast)
            print("Result:", result)
        except Exception as e:
            print("Exception during eval:", type(e).__name__, e)
            print(traceback.format_exc(limit=2))
            traceback.print_exc()
    except Exception as e:
        print("Exception during parse:", type(e).__name__, e)
        print(traceback.format_exc(limit=2))

def run_debug_module():
    CASES = [
        "(10 + 5);",
        "$math1: (10); $math2: (5); ($math1 + $math2);",
        '"2 times 2 is <(2*2)>.";',
        # Add more minimal or pathological cases as you need!
    ]
    for src in CASES:
        debug_case(src)
    print("=" * 60)
    print("[debug-module.py] End of debug output.\n")


if __name__ == "__main__":
    run_debug_module()
