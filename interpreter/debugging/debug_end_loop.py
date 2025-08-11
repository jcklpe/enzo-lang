#!/usr/bin/env python3
"""Debug end-loop behavior"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
$numbers: [1, 8];
Loop for $num in $numbers, (
    If $num is 8, (
        "Found 8, ending loop.";
        end-loop;
    );
    "Processing: <$num>";
);
'''

print("Testing end-loop behavior...")
print("=" * 50)

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
