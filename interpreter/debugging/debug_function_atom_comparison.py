#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

def debug_comparison():
    test_code = '''
    If (5) is 5, ("SUCCESS: Function atom comparison works");
    '''

    try:
        parser = Parser(test_code)
        ast = parser.parse()

        print("=== PARSED AST ===")
        print("Program statements:")
        for i, stmt in enumerate(ast.statements if hasattr(ast, 'statements') else [ast]):
            print(f"  {i}: {stmt}")
            if hasattr(stmt, 'condition'):
                print(f"    condition: {stmt.condition}")
                if hasattr(stmt.condition, 'left'):
                    print(f"      left: {stmt.condition.left}")
                if hasattr(stmt.condition, 'operator'):
                    print(f"      operator: {stmt.condition.operator}")
                if hasattr(stmt.condition, 'right'):
                    print(f"      right: {stmt.condition.right}")

        print("\n=== EVALUATION ===")
        result = eval_ast(ast)
        print('Result:', result)

    except Exception as e:
        print('Error:', e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_comparison()
