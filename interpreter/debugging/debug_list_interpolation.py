#!/usr/bin/env python3
"""Debug list interpolation parsing"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing list interpolation parsing...")
print("=" * 50)

test_code = '''
$dynamic-list: [1, 2, 3];
[<$dynamic-list>, 4] :> $dynamic-list;
$dynamic-list;
'''

try:
    print("Parsing code:")
    print(test_code)
    ast = parse(test_code)
    print("✓ Parsing successful!")
    print("AST:", ast)

    print("\nEvaluating...")
    result = eval_ast(ast)
    print("✓ Evaluation successful!")
    print("Result:", result)
except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
