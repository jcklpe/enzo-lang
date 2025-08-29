#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test conditional with variable shadowing similar to the failing case
test_content = '''$scope-test: "global";
If False, (
    $if-var: 1;
), Else, (
    $scope-test: "else-branch";
    "In Else: <$scope-test>";
);
"Afterward: <$scope-test>";
'''

test_file = '/tmp/test_shadowing_conditional.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing conditional with shadowing (no error) ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("Visual output:")
print(result.stdout)

# Now add the error case
test_content2 = '''$scope-test: "global";
If False, (
    $if-var: 1;
), Else, (
    $scope-test: "else-branch";
    "In Else: <$scope-test>";
    $if-var;
);
"Afterward: <$scope-test>";
'''

test_file2 = '/tmp/test_shadowing_with_error.enzo'
with open(test_file2, 'w') as f:
    f.write(test_content2)

print("=== Testing conditional with shadowing and error ===")
result2 = subprocess.run(['poetry', 'run', 'enzo', test_file2],
                        capture_output=True, text=True, cwd='.')

print("Visual output:")
print(result2.stdout)
