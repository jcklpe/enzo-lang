#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env

# Reset environment for clean testing
_env.clear()

# Test parameter syntax
test_code = '''
@test-func: (
    param @x: 6;
    param @y: 4;
    return($x + $y);
);
$test-func();
'''

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

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
