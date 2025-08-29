#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the exact TYPE CONSISTENCY ON REBINDING case
test_content = '''$result-33: 100;
$result-33; // prints 100
$result-33 <: If False, (300), Else, ("error-type"); // error: cannot bind Text to Number
'''

test_file = '/tmp/test_type_consistency.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing TYPE CONSISTENCY ON REBINDING ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("STDERR:")
print(repr(result.stderr))
print("Return code:", result.returncode)
print("Visual output:")
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr)
