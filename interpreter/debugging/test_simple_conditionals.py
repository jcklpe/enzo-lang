#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test simple conditional execution
test_content = '''If True, (
    "This should print";
);
"After conditional";
'''

test_file = '/tmp/test_simple_conditional.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing simple conditional ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("Visual output:")
print(result.stdout)

# Test simple else block
test_content2 = '''If False, (
    "This should NOT print";
), Else, (
    "This SHOULD print";
);
"After conditional";
'''

test_file2 = '/tmp/test_else_conditional.enzo'
with open(test_file2, 'w') as f:
    f.write(test_content2)

print("=== Testing else conditional ===")
result2 = subprocess.run(['poetry', 'run', 'enzo', test_file2],
                        capture_output=True, text=True, cwd='.')

print("Visual output:")
print(result2.stdout)
