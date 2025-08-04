import sys
sys.path.insert(0, '.')

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast

# Test parsing and evaluation of the problematic if statement
code = "If True, ($test-var: 42; $test-var);"
ast = parse(code)
print(f"AST: {ast}")
print(f"AST type: {type(ast)}")

if hasattr(ast, 'then_block'):
    print(f"Then block: {ast.then_block}")
    print(f"Then block length: {len(ast.then_block)}")
    for i, stmt in enumerate(ast.then_block):
        print(f"Statement {i}: {stmt} (type: {type(stmt)})")
