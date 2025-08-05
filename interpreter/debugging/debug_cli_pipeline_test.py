#!/usr/bin/env python3
import subprocess
import os

# Test if the conditional pipelining code is somehow consuming the next comment
test_file_content = '''//= Conditional pipelining
$goblinoid: [
  $health: 30,
  $status: "alive"
];

$goblinoid.health;
$goblinoid.status;

//= IF CONDITION WITH NESTED LIST INDEX ACCESS
$nested-list: [["zero", "one"], ["two", "three"]];

If $nested-list.1.0 is "two", (
  say("Nested index matched 'two'");
);
'''

# Write test file
with open('/tmp/test_conditional_pipeline.enzo', 'w') as f:
    f.write(test_file_content)

# Run the interpreter
proc = subprocess.run(
    ["poetry", "run", "enzo", "/tmp/test_conditional_pipeline.enzo"],
    capture_output=True,
    text=True,
    cwd="/Users/aslan/work/enzo-lang/interpreter"
)

print("=== STDOUT ===")
print(repr(proc.stdout))
print("\n=== STDERR ===")
print(repr(proc.stderr))
print(f"\n=== EXIT CODE: {proc.returncode} ===")

# Split by //= to see if boundaries are preserved
lines = proc.stdout.splitlines()
print(f"\n=== OUTPUT LINES ({len(lines)}) ===")
for i, line in enumerate(lines):
    print(f"{i}: {repr(line)}")
