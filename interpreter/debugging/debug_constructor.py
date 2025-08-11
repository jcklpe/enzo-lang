#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse
from src.runtime_helpers import EnzoList

# Reset environment for clean testing
_env.clear()

# Test EnzoList constructor directly
print("=== Testing EnzoList constructor directly ===")
test_list = EnzoList(is_blueprint_instance=True, blueprint_name="TestBlueprint")
print(f"Direct constructor test:")
print(f"  _is_blueprint_instance: {test_list._is_blueprint_instance}")
print(f"  _blueprint_name: {test_list._blueprint_name}")
print(f"  repr: {repr(test_list)}")

print("\n=== Testing through evaluator ===")

test_code = '''
Player: <[ name: Text, hp: Number ]>;
$test_player: Player[$name: "Test", $hp: 50];
'''

try:
    ast = parse(test_code)
    print("Parsing successful!")

    # Add some debug info by patching the evaluator temporarily
    import src.evaluator as evaluator_module
    original_eval = evaluator_module.eval_ast

    def debug_eval(*args, **kwargs):
        result = original_eval(*args, **kwargs)
        # Check if this is a blueprint instantiation result
        if hasattr(result, '_is_blueprint_instance') and result._is_blueprint_instance:
            print(f"DEBUG: Created blueprint instance with name: {result._blueprint_name}")
        return result

    evaluator_module.eval_ast = debug_eval

    try:
        result = eval_ast(ast)

        # Check the test_player variable
        test_player = _env.get('test_player') or _env.get('$test_player')
        print(f"test_player: {test_player}")
        print(f"test_player type: {type(test_player)}")
        if hasattr(test_player, '_is_blueprint_instance'):
            print(f"test_player._is_blueprint_instance: {test_player._is_blueprint_instance}")
        if hasattr(test_player, '_blueprint_name'):
            print(f"test_player._blueprint_name: {test_player._blueprint_name}")
        print(f"test_player repr: {repr(test_player)}")

    finally:
        # Restore original eval function
        evaluator_module.eval_ast = original_eval

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
