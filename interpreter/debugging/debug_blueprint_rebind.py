#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

test_code = '''
Player: <[ name: Text, hp: Number ]>;

$monsters: [
    Player[$name: "Goblin", $hp: 20],
    Player[$name: "Orc", $hp: 50]
];

$monsters;

// Test simple blueprint instantiation first
$new_player: Player[$name: "Super Orc", $hp: 100];
$new_player;

// Test the problematic rebinding line
Loop for @monster_ref in $monsters, (
    If $monster_ref.name is "Orc", (
        Player[$name: "Super Orc", $hp: 100] :> $monster_ref;
    );
);

$monsters;
'''

try:
    print("=== Parsing test code ===")
    ast = parse(test_code)
    print("Parsing successful!")

    print("\n=== Evaluating test code ===")
    result = eval_ast(ast)
    print(f"Result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
