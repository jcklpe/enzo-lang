#!/usr/bin/env python3

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

# Debug restart-loop step by step
test_code = '''
$count: 1;
Loop, (
    $count;
    If $count is 2, (
        "About to restart";
        restart-loop;
    );
    "After if check";
    $count <: $count + 1;
    If $count is 4, (
        end-loop;
    );
);
'''

def debug_step():
    try:
        parser = Parser(test_code)
        ast = parser.parse()

        print("AST for loop body:")
        if hasattr(ast, 'statements'):
            for i, stmt in enumerate(ast.statements):
                print(f"  {i}: {stmt}")
                if hasattr(stmt, 'body'):
                    for j, body_stmt in enumerate(stmt.body):
                        print(f"    body[{j}]: {body_stmt}")

        print("\nExecuting with debug output...")
        result = eval_ast(ast)
        print('Restart-loop test results:', result)

    except Exception as e:
        print('Error:', e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_step()
