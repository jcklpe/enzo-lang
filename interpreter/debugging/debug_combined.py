#!/usr/bin/env python3

import subprocess
import os

def test_combined_directly():
    # Run just the first few lines of the combined test to isolate the issue
    test_content = '''//= INVOKING AN UNDEFINED VARIABLE
$undefinedVar;

//= EMPTY BIND ────────────────────────────────────────────────────────────
$x: ;

//= REDECLARING A VARIABLE (USING ":") ERRORS ────────────────────────────
$x: 10;
'''

    # Write to a temporary file
    with open("/tmp/debug_combined.enzo", "w") as f:
        f.write(test_content)

    print("=== Testing first few blocks of combined test ===")
    proc = subprocess.run(
        ["poetry", "run", "enzo", "/tmp/debug_combined.enzo"],
        capture_output=True,
        text=True,
        cwd="/Users/aslan/work/enzo-lang/interpreter"
    )

    print("STDOUT:")
    print(repr(proc.stdout))
    print("STDERR:")
    print(repr(proc.stderr))
    print(f"Return code: {proc.returncode}")

if __name__ == "__main__":
    test_combined_directly()
