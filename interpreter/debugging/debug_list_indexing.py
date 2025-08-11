#!/usr/bin/env python3
"""Debug list indexing in list construction"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing list indexing in list construction...")
print("=" * 50)

test_code = '''
$list-delete-behind: ["a", "b", "c"];
[$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
$list-delete-behind;
'''

try:
    print("Parsing code:")
    print(test_code)
    ast = parse(test_code)
    print("✓ Parsing successful!")

    print("\nEvaluating...")
    result = eval_ast(ast)
    print("✓ Evaluation successful!")
    print("Result:", result)

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
