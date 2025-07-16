#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse_program
from evaluator import eval_ast
from runtime_helpers import EnzoList

# Test the property access issue
src = """
$person6: [$name6: "Ali", $age6: 21];
$name6, $age6: $person6[];
$person6;
"""

print("Testing property access...")
try:
    program = parse_program(src)
    env = {}

    for stmt in program.statements:
        result = eval_ast(stmt, env=env)
        print("Result:", result)

    # Check what keys are in person6
    person6 = env.get('$person6')
    print("\n$person6:", person6)
    print("Type:", type(person6))
    if hasattr(person6, '_key_map'):
        print("Key map:", person6._key_map)
        print("Elements:", person6._elements)

        # Try accessing different keys
        for key in ['name', '$name', 'name6', '$name6']:
            try:
                val = person6.get_by_key(key)
                print(f"Key '{key}': {val}")
            except Exception as e:
                print(f"Key '{key}': {e}")

except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
