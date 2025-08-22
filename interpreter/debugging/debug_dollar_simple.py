#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

# Test just $foo by itself
test_code = '$foo;'

print(f"Test code: {test_code}")
print()

try:
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print("AST:", ast)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
