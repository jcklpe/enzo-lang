#!/usr/bin/env python3

# Test the _is_truthy function
import sys
sys.path.insert(0, '/Users/aslan/work/enzo-lang/interpreter/src')

from evaluator import _is_truthy

# Test cases that should be falsy
test_cases = [
    (0, "number 0"),
    ("", "empty string"),
    ([], "empty list"),
    ([0, 0, 0], "list of zeros"),
]

print("=== TESTING _is_truthy FUNCTION ===")
for value, description in test_cases:
    result = _is_truthy(value)
    expected = "falsy" if not result else "truthy"
    print(f"{description}: {result} ({expected})")

# Test what any() returns for list of zeros
print(f"\nany([False, False, False]): {any([False, False, False])}")
print(f"any(_is_truthy(item) for item in [0,0,0]): {any(_is_truthy(item) for item in [0,0,0])}")
