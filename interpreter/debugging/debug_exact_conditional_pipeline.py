#!/usr/bin/env python3
import subprocess
import os

# Test the exact conditional pipelining section
test_file_content = '''//= Conditional pipelining
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
'''

# Write test file
with open('/tmp/test_exact_conditional_pipeline.enzo', 'w') as f:
    f.write(test_file_content)

# Run the interpreter
proc = subprocess.run(
    ["poetry", "run", "enzo", "/tmp/test_exact_conditional_pipeline.enzo"],
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
