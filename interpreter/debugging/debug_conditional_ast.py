#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse
from src.enzo_parser.ast_nodes import *

# Reset environment
_env.clear()

print("=== Examining AST Structure ===")

# Parse a simple conditional to see its structure
test_code = """
$x: "global";
If True, (
    $x: "shadowed";
    $x;
);
$x;
"""

try:
    ast = parse(test_code)
    print("Full AST:")
    print(f"Type: {type(ast)}")

    # Handle both list and Program object cases
    if isinstance(ast, list):
        statements = ast
        print(f"Statements: {len(statements)}")
    else:
        statements = ast.statements
        print(f"Statements: {len(statements)}")

    for i, stmt in enumerate(statements):
        print(f"\nStatement {i}: {type(stmt)}")
        if isinstance(stmt, IfStatement):
            print(f"  Condition: {stmt.condition} (type: {type(stmt.condition)})")
            print(f"  Then block: {stmt.then_block} (type: {type(stmt.then_block)})")

            # Check if then_block is a FunctionAtom
            if hasattr(stmt.then_block, 'statements'):
                print(f"  Then block statements: {len(stmt.then_block.statements)}")
                for j, block_stmt in enumerate(stmt.then_block.statements):
                    print(f"    Block statement {j}: {type(block_stmt)}")
                    if isinstance(block_stmt, Binding):
                        print(f"      Binding: {block_stmt.keyname} = {block_stmt.value}")

            print(f"  Else block: {stmt.else_block}")
            print(f"  Else if chain: {getattr(stmt, 'else_if_chain', None)}")

        elif isinstance(stmt, Binding):
            print(f"  Binding: {stmt.keyname} = {stmt.value}")
        elif isinstance(stmt, VarInvoke):
            print(f"  VarInvoke: {stmt.keyname}")

except Exception as e:
    print("Parse error:", e)
    import traceback
    traceback.print_exc()
