#!/usr/bin/env python3

import subprocess
import os

def test_vars_direct():
    # Run the vars module directly (this works)
    print("=== Testing vars module directly ===")
    proc = subprocess.run(
        ["poetry", "run", "enzo", "tests/test-modules/vars.enzo"],
        capture_output=True,
        text=True,
        cwd="/Users/aslan/work/enzo-lang/interpreter"
    )

    print("STDOUT:")
    print(proc.stdout)
    print("STDERR:")
    print(proc.stderr)
    print(f"Return code: {proc.returncode}")

if __name__ == "__main__":
    test_vars_direct()
