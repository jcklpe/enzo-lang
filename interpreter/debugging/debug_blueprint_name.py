#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

test_code = '''
Player: <[ name: Text, hp: Number ]>;
$test_player: Player[$name: "Test", $hp: 50];
'''

print("=== Debugging blueprint name passing ===")

try:
    ast = parse(test_code)
    print("Parsing successful!")

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

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
