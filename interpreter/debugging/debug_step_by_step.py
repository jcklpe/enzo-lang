#!/usr/bin/env python3
import subprocess
import os

# Test different ways of writing the conditional pipeline
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

$goblinoid.health;
$goblinoid.status;

//= Next section
$test: "after";
'''

# Write test file
with open('/tmp/test_debug_goblinoid.enzo', 'w') as f:
    f.write(test_file_content)

# Run the interpreter
proc = subprocess.run(
    ["poetry", "run", "enzo", "/tmp/test_debug_goblinoid.enzo"],
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
