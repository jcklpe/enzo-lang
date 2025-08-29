#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the exact SCOPE ISOLATION: Else if section
test_content = '''//= SCOPE ISOLATION: `Else if` HAS ITS OWN ISOLATED SCOPE
$level-scope: 1;
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

test_file = '/tmp/test_else_if_isolation.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing ELSE IF ISOLATION section ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("STDERR:")
print(repr(result.stderr))
print("Return code:", result.returncode)

print("\nVisual output:")
print(result.stdout)

# Count lines in output
lines = result.stdout.strip().split('\n')
print(f"\nNumber of lines: {len(lines)}")
for i, line in enumerate(lines):
    print(f"Line {i+1}: {repr(line)}")
