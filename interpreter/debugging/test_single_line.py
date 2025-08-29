#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test just the failing line to see what output it produces
test_file = '/tmp/test_zlocal.enzo'
with open(test_file, 'w') as f:
    f.write('$z-local; // error: undefined variable\n')

print("=== Testing single failing line ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("STDERR:")
print(repr(result.stderr))
print("Return code:", result.returncode)

print("\nVisual output:")
print(result.stdout)
