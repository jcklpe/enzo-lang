#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import just what we need without triggering CLI imports
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Avoid CLI imports by monkey-patching the format_val function
def simple_format_val(val):
    return str(val)

# Replace the CLI import in evaluator to avoid colorama dependency
import src.evaluator
import types
mock_cli = types.ModuleType('cli')
mock_cli.format_val = simple_format_val
sys.modules['src.cli'] = mock_cli

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Testing Fixed Variable Scoping in Student Blueprint ===")

# Test the exact Student blueprint code that was causing division by zero
student_code = '''
Student: <[
    name: "Unknown",
    scores: [],
    calculate_average: (
        $total: 0;
        $count: 0;
        Loop for $score in $self.scores, (
            $total + $score :> $total;
            $count + 1 :> $count;
        );
        $total / $count;
    )
]>;

$alice: Student[
    $name: "Alice",
    $scores: [95, 87, 92]
];

$alice.calculate_average();
'''

print("Student blueprint code:")
print(student_code)
print()

try:
    ast = parse(student_code)
    result = eval_ast(ast)
    print("✅ SUCCESS! Result:", result)
    print("Expected: ~91.33 (average of 95, 87, 92)")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing Our Original Debug Case ===")

# Reset environment
_env.clear()
_initialize_builtin_variants()

simple_test_code = '''
$test_loop: (
    $list: [1, 2, 3];
    $count: 0;
    Loop for $item in $list, (
        $count + 1 :> $count;
    );
    $count;
);

$test_loop();
'''

print("Simple test code:")
print(simple_test_code)
print()

try:
    ast = parse(simple_test_code)
    result = eval_ast(ast)
    print("✅ SUCCESS! Result:", result)
    print("Expected: 3")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
