#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

test_code = '''
Player: <[ name: Text, hp: Number ]>;

$player1: Player[$name: "Test", $hp: 50];
$player1;
'''

try:
    print("=== Testing blueprint printing ===")
    ast = parse(test_code)
    print("Parsing successful!")

    print("\n=== Evaluating test code ===")
    result = eval_ast(ast)
    print(f"Result: {result}")

    # Also test the direct instance
    print("\nDirect test of blueprint instance:")
    player = _env['player1']
    print(f"Player type: {type(player)}")
    print(f"Player._is_blueprint_instance: {player._is_blueprint_instance}")
    print(f"Player._blueprint_name: {player._blueprint_name}")
    print(f"Player repr: {repr(player)}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
