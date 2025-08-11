#!/usr/bin/env python3

import sys
sys.path.append('/Users/aslan/work/enzo-lang/interpreter/src')

from enzo_parser.parser import Parser
from evaluator import eval_ast, _env

# Test just the condition evaluation
code = '''
$goblinoid: [
  $health: 30,
  $status: "alive"
];

take-damage1: (
  param $target: ;
  param $damage: 0;
  $target.health - $damage :> $target.health;
  return($target);
);

$after_damage: $goblinoid then take-damage1($this, 30);

"After damage - health:";
$after_damage.health;
"After damage - status:";
$after_damage.status;

"Condition check:";
If $after_damage.health is less than 1, ("Condition is true"), Else, ("Condition is false");

"Manual check:";
If 0 is less than 1, ("Zero less than one is true"), Else, ("Zero less than one is false");
'''

try:
    parser = Parser(code)
    ast = parser.parse()
    env = _env.copy()  # Create a copy of the global environment

    result = eval_ast(ast, env=env)
    print("Final result:", result)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
