#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, ListElementReference
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, ListElementReference
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the ListElementReference class directly
print("=== Testing ListElementReference directly ===")
test_list = [10, 20, 30]
print(f"Original list: {test_list}")

ref = ListElementReference(test_list, 1)  # reference to index 1 (value 20)
print(f"Reference value: {ref.get_value()}")

ref.set_value(25)
print(f"After setting to 25: {test_list}")
print(f"Reference value: {ref.get_value()}")

# Test the for loop with reference
print("\n=== Testing for loop with reference ===")
test_code = """
$list-for-copy2: [10, 20, 30];
Loop for @item in $list-for-copy2, (
  $item;
);
"""

try:
    ast = parse(test_code)
    print(f"Parsed AST: {ast}")

    print(f"Loop type: {ast[1].loop_type}")
    print(f"Is reference: {ast[1].is_reference}")
    print(f"Variable: {ast[1].variable}")

    result = eval_ast(ast)
    print(f"Result: {result}")

    # Check the final state of the list
    print(f"Final list state: {_env.get('$list-for-copy2', 'NOT FOUND')}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test a simple rebinding case
print("\n=== Testing simple rebinding with reference ===")
test_code2 = """
$simple-list: [10, 20, 30];
Loop for @item in $simple-list, (
  $item <: $item + 1;
  $item;
);
$simple-list;
"""

try:
    _env.clear()  # Reset for clean test
    ast2 = parse(test_code2)
    result2 = eval_ast(ast2)
    print(f"Result: {result2}")

    # Check the final state of the list
    print(f"Final list state: {_env.get('$simple-list', 'NOT FOUND')}")

except Exception as e:
    print(f"Error in rebinding test: {e}")
    import traceback
    traceback.print_exc()

try:
    ast = parse(test_code)
    print(f"Parsed AST: {ast}")

    # The parser returns a Program node with a nodes list
    if hasattr(ast, 'nodes'):
        loop_node = ast.nodes[0]
    else:
        # If it's just a list, take the first element
        loop_node = ast[0] if isinstance(ast, list) else ast

    print(f"Loop type: {loop_node.loop_type}")
    print(f"Is reference: {loop_node.is_reference}")
    print(f"Variable: {loop_node.variable}")

    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
