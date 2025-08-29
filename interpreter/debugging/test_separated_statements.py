#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test with explicit statement separation
test_content = '''$level-scope: 1;

If $level-scope is 0, (
    $msg-scope: "Level 0";
), Else if $level-scope is 1, (
    $msg-scope: "Level 1"; // This shadows any outer $msg and is local to this block.
    "In Else If: <$msg-scope>"; // Prints "Level 1"
), Else, (
    $msg-scope: "Other Level";
);

$msg-scope; // error: undefined variable (each $msg was local to its own conditional block)
'''

test_file = '/tmp/test_separated_statements.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing with explicit statement separation ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("Visual output:")
print(result.stdout)
