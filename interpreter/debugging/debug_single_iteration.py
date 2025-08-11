#!/usr/bin/env python3
"""Debug the exact rebinding issue"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

# Test just the rebinding inside a single loop iteration
test_code = '''
$active-while: True;
$counter-while: 4;
"Before: active="; $active-while; "counter="; $counter-while;

$counter-while + 1 :> $counter-while;
"After increment: counter="; $counter-while;

If $counter-while is 5, (
    "Setting False";
    False :> $active-while;
    "Set to False";
);

"After: active="; $active-while; "counter="; $counter-while;
'''

print("Testing single iteration...")
print("=" * 50)

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
    print(f"Environment: active={_env.get('$active-while')}, counter={_env.get('$counter-while')}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
