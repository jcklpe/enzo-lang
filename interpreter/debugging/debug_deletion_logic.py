#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

test_code = '''
$x: ["a", "b", "c"];
Loop for $item in $x, (
    $item;
    If $item is "a", (
        [$x.2, $x.3] :> $x;
        "After deleting 'a', x is:";
        $x;
    );
);
'''

print("=== Parsing test code ===")
try:
    ast = parse(test_code)
    print("✓ Parsed successfully")
except Exception as e:
    print(f"✖ Parse error: {e}")
    sys.exit(1)

print("\n=== Evaluating test code ===")
try:
    result = eval_ast(ast)
    print(f"✓ Evaluation completed")
    print(f"Result: {result}")
except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
