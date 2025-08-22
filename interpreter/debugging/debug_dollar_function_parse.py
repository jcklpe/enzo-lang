#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.error_handling import EnzoParseError

# Test the exact pattern from functions test that's failing
test_code = """(@foo: 99; $foo)"""

print(f"Test code: {test_code}")
print()

try:
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print(f"AST: {ast}")
    print(f"AST statements: {ast.statements}")
    if ast.statements:
        print(f"First statement: {ast.statements[0]}")
        if hasattr(ast.statements[0], 'statements'):
            print(f"Function statements: {ast.statements[0].statements}")
except EnzoParseError as e:
    print("❌ Parse error:")
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    if hasattr(e, 'code_line'):
        print(f"Code line: {repr(e.code_line)}")
    if hasattr(e, 'token'):
        print(f"Token: {e.token}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
