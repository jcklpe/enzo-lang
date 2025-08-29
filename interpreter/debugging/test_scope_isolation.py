#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the SCOPE ISOLATION section specifically
test_content = '''//= SCOPE ISOLATION: `If` AND `Else` BLOCKS HAVE SEPARATE SCOPES
$scope-test: "global";
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

test_file = '/tmp/test_scope_isolation.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing SCOPE ISOLATION section ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("STDERR:")
print(repr(result.stderr))
print("Return code:", result.returncode)

print("\nVisual output:")
print(result.stdout)
