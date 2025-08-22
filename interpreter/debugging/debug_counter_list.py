#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env

# Reset environment for clean testing
_env.clear()

# Test the list with function member that's failing
test_code = '''
@counter: [
    @count: 10,
    @increment: (
        $self.count + 1 :> @self.count;
        return($self.count);
    )
];
$counter.count;
$counter.increment();
'''

print(f"Test code: {test_code}")
print()

try:
    ast = parse(test_code)
    print("✅ Parsing successful!")

    result = eval_ast(ast)
    print("✅ Evaluation successful!")
    print("Result:", result)

    # Check what's in the environment
    print()
    print("Environment:")
    for key, value in _env.items():
        print(f"  {key}: {value}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
