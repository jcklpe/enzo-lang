#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test simple else-if without errors
test_content = '''$level-scope: 1;
If $level-scope is 0, (
    "Level 0";
), Else if $level-scope is 1, (
    "Level 1";
), Else, (
    "Other Level";
);
"After conditional";
'''

test_file = '/tmp/test_simple_else_if.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing simple else-if ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("Visual output:")
print(result.stdout)

# Test else-if with variable interpolation (like the failing case)
test_content2 = '''$level-scope: 1;
If $level-scope is 0, (
    $msg: "Level 0";
    "In If: <$msg>";
), Else if $level-scope is 1, (
    $msg: "Level 1";
    "In Else If: <$msg>";
), Else, (
    $msg: "Other Level";
    "In Else: <$msg>";
);
"After conditional";
'''

test_file2 = '/tmp/test_else_if_with_vars.enzo'
with open(test_file2, 'w') as f:
    f.write(test_content2)

print("=== Testing else-if with variables ===")
result2 = subprocess.run(['poetry', 'run', 'enzo', test_file2],
                        capture_output=True, text=True, cwd='.')

print("Visual output:")
print(result2.stdout)
