#!/usr/bin/env python3
import subprocess
import os

# Test the goblinoid property access issue
test_file_content = '''$goblinoid: [
  $health: 30,
  $status: "alive"
];

$goblinoid.health;
$goblinoid.status;

take-damage1: (
  param $target: ;
  param $damage: 0;
  $target.health;
  $target.health - $damage;
  $target.health - $damage :> $target.health;
  return($target);
);

take-damage1($goblinoid, 30);
'''

# Write test file
with open('/tmp/test_goblinoid.enzo', 'w') as f:
    f.write(test_file_content)

# Run the interpreter
proc = subprocess.run(
    ["poetry", "run", "enzo", "/tmp/test_goblinoid.enzo"],
    capture_output=True,
    text=True,
    cwd="/Users/aslan/work/enzo-lang/interpreter"
)

print("=== STDOUT ===")
print(repr(proc.stdout))
print("\n=== STDERR ===")
print(repr(proc.stderr))
print(f"\n=== EXIT CODE: {proc.returncode} ===")
