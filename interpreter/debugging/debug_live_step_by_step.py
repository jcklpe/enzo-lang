#!/usr/bin/env python3
"""Debug live iteration step by step"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing live iteration step by step...")
print("=" * 50)

# Simpler test - just append and see if it's picked up
test_code = '''
$simple-list: [1, 2];
Loop for $item in $simple-list, (
    "Processing: <$item>";
    If $item is 2, (
        [<$simple-list>, 3] :> $simple-list;
        "Added 3, list is now: <$simple-list>";
    );
);
'''

try:
    print("Parsing and evaluating:")
    print(test_code)
    ast = parse(test_code)
    result = eval_ast(ast)
    print("✓ Complete!")

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
