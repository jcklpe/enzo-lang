#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the EXACT case from the failing test, including all comments
test_content = '''$scope-test: "global";
If False, (
    $scope-test: "if-branch"; // This block is not entered.
    $if-var: 1;
), Else, (
    $scope-test: "else-branch"; // Shadows the global variable.
    "In Else: <$scope-test>"; // Prints "else-branch"
    $if-var; // error: undefined variable (was defined in a separate scope)
);
"Afterward: <$scope-test>"; // Global is untouched. Prints "global"
'''

test_file = '/tmp/test_exact_failing_case.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing EXACT failing case ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("Visual output:")
print(result.stdout)

# Also test line by line to see where the issue occurs
test_lines = [
    '$scope-test: "global";',
    'If False, (\n    $scope-test: "if-branch";\n    $if-var: 1;\n), Else, (\n    $scope-test: "else-branch";\n    "In Else: <$scope-test>";\n    $if-var;\n);',
    '"Afterward: <$scope-test>";'
]

print("\n=== Testing line by line ===")
for i, line in enumerate(test_lines):
    test_file_line = f'/tmp/test_line_{i}.enzo'
    with open(test_file_line, 'w') as f:
        f.write('\n'.join(test_lines[:i+1]))

    result_line = subprocess.run(['poetry', 'run', 'enzo', test_file_line],
                                capture_output=True, text=True, cwd='.')
    print(f"After line {i}: {repr(result_line.stdout)}")
