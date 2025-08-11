#!/usr/bin/env python3
"""Debug simple live iteration step by step"""

import sys
sys.path.append('..')

# Let's test this manually to understand the expected behavior
print("Manual test of live iteration with deletion...")
print("=" * 50)

# Simulate the test case step by step
original_list = ["a", "b", "c"]
visited = []

print("Initial state:")
print(f"  List: {original_list}")
print(f"  Visited: {visited}")
print()

# Iteration 1: i=0, item="a"
print("Iteration 1: i=0")
item = original_list[0]  # "a"
print(f"  Processing: {item}")
visited.append(item)
print(f"  Visited: {visited}")
print(f"  List after: {original_list}")
print()

# Iteration 2: i=1, item="b"
print("Iteration 2: i=1")
item = original_list[1]  # "b"
print(f"  Processing: {item}")
visited.append(item)
print(f"  Visited: {visited}")

# Delete "a" - take elements 2 and 3 (1-indexed = indices 1 and 2)
print("  Deleting 'a' - taking elements 2 and 3")
original_list = [original_list[1], original_list[2]]  # ["b", "c"]
print(f"  List after deletion: {original_list}")
print()

# Iteration 3: i=2, but list is now ["b", "c"]
print("Iteration 3: i=2")
print(f"  Current list: {original_list}")
print(f"  List length: {len(original_list)}")
print(f"  Index 2 >= length 2? {2 >= len(original_list)}")

if 2 >= len(original_list):
    print("  Would break here in current implementation")
else:
    item = original_list[2]
    print(f"  Processing: {item}")
    visited.append(item)

print()
print("Expected result:")
print(f"  Visited: ['a', 'b', 'c']")
print(f"  Actual visited: {visited}")
print(f"  Final list: ['b', 'c']")
print(f"  Actual list: {original_list}")
