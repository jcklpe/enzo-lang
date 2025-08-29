#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the type mismatch error to see if capitalization is fixed
test_content = '''$adder: (Number $x: 0, Number $y: 0) -> $x + $y;
$adder("", 500);  // error: expected argument is a Number atom, not a Text atom
'''

test_file = '/tmp/test_type_mismatch.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing type mismatch error capitalization ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("Visual output:")
print(result.stdout)
