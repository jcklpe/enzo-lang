#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the exact WHILE LOOP WITH COMPLEX CONDITION case
test_content = '''$active-while: True;
$counter-while: 0;
Loop while $active-while and $counter-while is less than 5, (
    $counter-while + 1 :> $counter-while;
    "Counter: <$counter-while>";

    If $counter-while is 5, (
        False :> $active-while;
    );
);
$active-while;
'''

test_file = '/tmp/test_while_complex.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing WHILE LOOP WITH COMPLEX CONDITION ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("Visual output:")
print(result.stdout)

# Also test a simpler case to see if loop variable modification works
test_simple = '''$x: 1;
Loop while $x is less than 3, (
    "x is <$x>";
    $x + 1 :> $x;
);
$x;
'''

test_file_simple = '/tmp/test_while_simple.enzo'
with open(test_file_simple, 'w') as f:
    f.write(test_simple)

print("\n=== Testing simple while loop variable modification ===")
result_simple = subprocess.run(['poetry', 'run', 'enzo', test_file_simple],
                              capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result_simple.stdout))
print("Visual output:")
print(result_simple.stdout)
