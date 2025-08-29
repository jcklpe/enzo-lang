#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test the exact failing else-if case, step by step
print("=== Step 1: Just the conditional without the error ===")
test_content1 = '''$level-scope: 1;
If $level-scope is 0, (
    $msg-scope: "Level 0";
), Else if $level-scope is 1, (
    $msg-scope: "Level 1";
    "In Else If: <$msg-scope>";
), Else, (
    $msg-scope: "Other Level";
);
'''

test_file1 = '/tmp/test_exact_else_if_step1.enzo'
with open(test_file1, 'w') as f:
    f.write(test_content1)

result1 = subprocess.run(['poetry', 'run', 'enzo', test_file1],
                        capture_output=True, text=True, cwd='.')
print("Output:")
print(repr(result1.stdout))

print("\n=== Step 2: Add the error line ===")
test_content2 = '''$level-scope: 1;
If $level-scope is 0, (
    $msg-scope: "Level 0";
), Else if $level-scope is 1, (
    $msg-scope: "Level 1";
    "In Else If: <$msg-scope>";
), Else, (
    $msg-scope: "Other Level";
);
$msg-scope;
'''

test_file2 = '/tmp/test_exact_else_if_step2.enzo'
with open(test_file2, 'w') as f:
    f.write(test_content2)

result2 = subprocess.run(['poetry', 'run', 'enzo', test_file2],
                        capture_output=True, text=True, cwd='.')
print("Output:")
print(repr(result2.stdout))

print("\n=== Step 3: The exact case with comments ===")
test_content3 = '''$level-scope: 1;
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

test_file3 = '/tmp/test_exact_else_if_step3.enzo'
with open(test_file3, 'w') as f:
    f.write(test_content3)

result3 = subprocess.run(['poetry', 'run', 'enzo', test_file3],
                        capture_output=True, text=True, cwd='.')
print("Output:")
print(repr(result3.stdout))
