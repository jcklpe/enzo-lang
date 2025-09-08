#!/usr/bin/env python3

from collections import ChainMap

# Test what happens when we copy a ChainMap
original_env = {'$count': 0}
chainmap_env = ChainMap({}, original_env)

print("Original ChainMap:")
print(f"chainmap_env: {dict(chainmap_env)}")
print(f"chainmap_env.maps: {chainmap_env.maps}")
print(f"Type: {type(chainmap_env)}")

# This is what the loop does
copied_env = chainmap_env.copy()

print("\nAfter .copy():")
print(f"copied_env: {copied_env}")
print(f"Type: {type(copied_env)}")

# Test updating both
print("\nUpdating $count in both environments:")
chainmap_env['$count'] = 5
copied_env['$count'] = 10

print(f"original_env: {original_env}")
print(f"chainmap_env: {dict(chainmap_env)}")
print(f"copied_env: {copied_env}")

print("\nThe copy loses the ChainMap structure and connection to original!")
