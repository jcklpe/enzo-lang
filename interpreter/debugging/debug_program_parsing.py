#!/usr/bin/env python3

import sys
sys.path.append('src')

from src.enzo_parser.parser import parse_program, parse
from src.evaluator import eval_ast

def debug_program_parsing():
    statement = '''If $status-if,
  "Ready!"; // should print "Ready!"
end;'''

    print("=== DEBUGGING PROGRAM PARSING ===")
    print(f"Statement:\n{repr(statement)}")

    # Test parse_program
    print("\n=== USING parse_program ===")
    try:
        program_ast = parse_program(statement)
        print(f"Program AST: {program_ast}")
        print(f"Program AST type: {type(program_ast)}")

        if hasattr(program_ast, 'statements'):
            print(f"Program statements: {program_ast.statements}")
            for i, stmt in enumerate(program_ast.statements):
                print(f"  Statement {i}: {stmt}")
    except Exception as e:
        print(f"parse_program failed: {e}")
        import traceback
        traceback.print_exc()

    # Test regular parse
    print("\n=== USING parse ===")
    try:
        regular_ast = parse(statement)
        print(f"Regular AST: {regular_ast}")
        print(f"Regular AST type: {type(regular_ast)}")
    except Exception as e:
        print(f"parse failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_program_parsing()
