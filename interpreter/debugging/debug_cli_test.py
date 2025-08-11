#!/usr/bin/env python3
import subprocess
import sys
import os

# Test just the specific failing block
test_content = '''//= FOR LOOP WITH END-LOOP
$numbers: [1, 2, 3, 4, 5];
Loop for $num in $numbers, (
    $num;
    If $num is 3, (end-loop;);
);
// Should print: 1, 2, 3
'''

# Write to a temporary file
with open('temp_test.enzo', 'w') as f:
    f.write(test_content)

# Run through enzo CLI
proc = subprocess.run(
    ["poetry", "run", "enzo", "temp_test.enzo"],
    capture_output=True,
    text=True,
    cwd="/Users/aslan/work/enzo-lang/interpreter"
)

print("=== CLI Output ===")
print(repr(proc.stdout))
print("=== CLI Stderr ===")
print(repr(proc.stderr))

# Clean up
os.unlink('temp_test.enzo')
