#!/usr/bin/env python3
import subprocess
import difflib
import os
import sys

# 1) Path to your .enzo test suite, now inside the tests/ folder
TEST_FILE   = os.path.join("tests", "combined-tests.enzo")

# 2) Path to the golden file you want to compare against
GOLDEN_FILE = os.path.join("tests", "combined-tests.golden.enzo")

def main():
    if not os.path.exists(TEST_FILE):
        print(f"❗ Test file not found: {TEST_FILE}")
        sys.exit(1)

    # Run your interpreter via Poetry, feeding it the TEST_FILE
    proc = subprocess.run(
        ["poetry", "run", "enzo", TEST_FILE],
        capture_output=True,
        text=True
    )

    actual = proc.stdout.rstrip("\n")

    if not os.path.exists(GOLDEN_FILE):
        print(f"❗ Golden file not found: {GOLDEN_FILE}")
        sys.exit(1)

    with open(GOLDEN_FILE) as f:
        expected = f.read().rstrip("\n")

    if actual == expected:
        print(f"✅ {TEST_FILE} matches golden file.")
        sys.exit(0)
    else:
        print(f"❌ {TEST_FILE} does NOT match golden file.")
        print()
        for line in difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        ):
            print(line)
        sys.exit(1)

if __name__ == "__main__":
    main()
