#!/usr/bin/env python3

# Simple test to debug IfStatement import issue

if __name__ == "__main__":
    try:
        from src.enzo_parser.ast_nodes import IfStatement, ComparisonExpression, LogicalExpression, NotExpression
        print("✓ Successfully imported control flow AST classes")
        print(f"IfStatement: {IfStatement}")
        print(f"ComparisonExpression: {ComparisonExpression}")
        print(f"LogicalExpression: {LogicalExpression}")
        print(f"NotExpression: {NotExpression}")
    except ImportError as e:
        print(f"✗ Import error: {e}")

    # Test parsing a simple IF statement
    try:
        from src.enzo_parser.parser import Parser
        code = 'If $status-if, "Ready!"; end;'
        parser = Parser(code)
        print(f"\nParsing: {code}")
        print(f"Tokens: {[(t.type, t.value) for t in parser.tokens]}")
        ast = parser.parse()
        print(f"AST: {ast}")
    except Exception as e:
        print(f"✗ Parsing error: {e}")
        import traceback
        traceback.print_exc()
