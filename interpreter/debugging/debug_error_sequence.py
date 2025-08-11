#!/usr/bin/env python3
import subprocess
import os

# Test the exact sequence: error test followed by conditional pipelining
test_file_content = '''//= ERROR: USING "is" WITH A VARIANT THAT DOES NOT EXIST
If $status-bp is StatusVariantBP.Unknown, (// error: undefined variable
  "Won't print";
);

//= Conditional pipelining
$goblinoid: [
  $health: 30,
  $status: "alive"
];

take-damage1: (
  param $target: ;
  param $damage: 0;
  $target.health - $damage :> $target.health;
  return($target);
);

set-status: (
  param $target: ;
  param $status: "";
  $status :> $target.status;
  return($target)
);

$goblinoid
  then take-damage1($this, 30)
    then If $this.health is less than 1, (
        set-status($this, "dead")
    )
  :> $goblinoid;

$goblinoid.health;  // should print 0
$goblinoid.status;  // should print "dead"

//= Next section
$test: "after";
'''

# Write test file
with open('/tmp/test_error_sequence.enzo', 'w') as f:
    f.write(test_file_content)

# Run the interpreter
proc = subprocess.run(
    ["poetry", "run", "enzo", "/tmp/test_error_sequence.enzo"],
    capture_output=True,
    text=True,
    cwd="/Users/aslan/work/enzo-lang/interpreter"
)

print("=== STDOUT ===")
print(repr(proc.stdout))
print("\n=== STDERR ===")
print(repr(proc.stderr))
print(f"\n=== EXIT CODE: {proc.returncode} ===")

if proc.stdout:
    lines = proc.stdout.splitlines()
    print(f"\n=== OUTPUT LINES ({len(lines)}) ===")
    for i, line in enumerate(lines):
        print(f"{i}: {repr(line)}")

# Test runner split
print("\n=== TESTING SPLIT_BLOCKS ===")
import sys
sys.path.append('/Users/aslan/work/enzo-lang/interpreter')
from run_tests import split_blocks

blocks = split_blocks(proc.stdout)
for i, (title, lines) in enumerate(blocks):
    print(f"Block {i}: '{title}' -> {len(lines)} lines")
    for j, line in enumerate(lines):
        print(f"  {j}: {repr(line)}")
