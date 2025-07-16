#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse_program
from evaluator import eval_ast
from runtime_helpers import EnzoList

# Test simple destructuring
src = """
$person1: [
  $name1: "Todd",
  $age1: 27,
  $favorite-color1: "blue"
];
$name1, $age1, $favorite-color1: $person1[];
"""

print("Testing simple destructuring...")
print("Source:", repr(src))

try:
    program = parse_program(src)
    print("Program AST:", program)

    # Create test environment
    env = {}

    # Execute the first statement (creating $person1)
    stmt1 = program.statements[0]  # $person1: [...]
    print("\nExecuting first statement:", stmt1)
    result1 = eval_ast(stmt1, env=env)
    print("Result1:", result1)
    print("Environment after first statement:", env)

    # Check what $person1 contains
    person1 = env.get('$person1')
    print("\n$person1 value:", person1)
    print("$person1 type:", type(person1))
    print("Has elements?", hasattr(person1, 'elements'))
    if hasattr(person1, 'elements'):
        print("Elements:", person1.elements)
    print("Is EnzoList?", isinstance(person1, EnzoList))

    # Try to get by key
    if isinstance(person1, EnzoList):
        try:
            name_val = person1.get_by_key('$name1')
            print("$name1 from list:", name_val)
        except Exception as e:
            print("Error getting $name1:", e)

    # Execute the second statement (destructuring)
    stmt2 = program.statements[1]  # $name1, $age1, ...
    print("\nExecuting second statement:", stmt2)
    result2 = eval_ast(stmt2, env=env)
    print("Result2:", result2)
    print("Environment after second statement:", {k: v for k, v in env.items() if k.startswith('$name') or k.startswith('$age') or k.startswith('$favorite')})

except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
