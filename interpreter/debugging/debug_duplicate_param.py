#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

# Test duplicate parameter error
test_code = '''
@duplicate-params: (
    param @x: 1;
    param @x: 2;
    return($x);
);
'''

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
