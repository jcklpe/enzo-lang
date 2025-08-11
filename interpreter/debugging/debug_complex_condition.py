#!/usr/bin/env python3
"""Debug complex condition while loop"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
# Re-initialize built-in variants like True/False
_initialize_builtin_variants()

test_code = '''
$active-while: True;
$counter-while: 0;
"Starting with active="; $active-while; "and counter="; $counter-while;

Loop while $active-while and $counter-while is less than 5, (
    "Iteration start: active="; $active-while; "counter="; $counter-while;
    $counter-while + 1 :> $counter-while;
    "After increment: counter="; $counter-while;
    "Counter: <$counter-while>";

    If $counter-while is 5, (
        "Setting active to False";
        False :> $active-while;
        "Active is now:"; $active-while;
    );
    "Iteration end: active="; $active-while; "counter="; $counter-while;
);
"Final: active="; $active-while; "counter="; $counter-while;
$active-while;
'''

print("Testing complex condition while loop...")
print("=" * 50)

try:
    ast = parse(test_code)
    print("Parsed successfully")

    print("\nEvaluating:")
    result = eval_ast(ast)
    print(f"Final result: {result}")

    print(f"\nEnvironment state:")
    print(f"$active-while = {_env.get('$active-while', 'UNDEFINED')}")
    print(f"$counter-while = {_env.get('$counter-while', 'UNDEFINED')}")

except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()

    # Check environment state even if error occurred
    print(f"\nEnvironment state at error:")
    for key, value in _env.items():
        print(f"{key} = {value}")
