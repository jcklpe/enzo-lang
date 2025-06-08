#!/usr/bin/env python3
import subprocess, difflib, os, sys

# 1) This is the single .enzo file you want to test
TEST_FILE = "tests.enzo"

# 2) This is where your golden output lives
GOLDEN_FILE = os.path.join("tests", "golden-files", "tests.enzo")

def main():
    # Run your interpreter via poetry
    proc = subprocess.run(
        ["poetry", "run", "enzo", TEST_FILE],
        capture_output=True, text=True
    )

    actual = proc.stdout.rstrip("\n")
    if not os.path.exists(GOLDEN_FILE):
        print(f"❗ Golden file not found at {GOLDEN_FILE}")
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
