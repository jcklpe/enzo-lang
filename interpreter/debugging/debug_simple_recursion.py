#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = """
$rec_n: 100;
rec_countdown: (
    param $rec_n: ;
    $rec_n;
    If $rec_n is greater than 0, (
        $rec_n - 1 :> $rec_n;
        rec_countdown($rec_n);
    );
);

rec_countdown(3);
"Global n is still: <$rec_n>";
"""

print("Parsing...")
ast = parse(test_code)

print("Executing...")
try:
    results = eval_ast(ast)
    print(f"Results: {results}")
    if isinstance(results, list):
        print(f"All results: {results}")
        for i, result in enumerate(results):
            if result is not None:
                print(f"  Result {i}: {result}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print(f"\nGlobal environment after execution:")
print(f"rec_n value: {_env.get('rec_n', 'NOT FOUND')}")
print(f"$rec_n value: {_env.get('$rec_n', 'NOT FOUND')}")
