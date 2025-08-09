#!/usr/bin/env python3
"""Debug simple end-loop case"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
Loop for $num in [8], (
    If $num is 8, (
        "Found 8!";
        end-loop;
    );
);
'''

print("Testing simple end-loop case...")
print("=" * 50)

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
