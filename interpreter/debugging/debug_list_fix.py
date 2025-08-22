#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env

# Reset environment for clean testing
_env.clear()

# Test the problematic list syntax
test_code = '@myList-text: [@greeting: "hi", @nums: [2, 4]];'

print(f"Test code: {test_code}")
print()

try:
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print("AST:", ast)
    print()

    result = eval_ast(ast)
    print("✅ Evaluation successful!")
    print("Result:", result)

    # Check what's in the environment
    print()
    print("Environment:")
    for key, value in _env.items():
        print(f"  {key}: {value}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
