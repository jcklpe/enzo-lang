#!/usr/bin/env python3

import sys
sys.path.append('/Users/aslan/work/enzo-lang/interpreter/src')

from enzo_parser.parser import Parser
from evaluator import eval_ast, _env

# Test the pipeline with If statement
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

set-status: (
  param $target: ;
  param $status: "";
  $status :> $target.status;
  return($target)
);

$result: $goblinoid
  then take-damage1($this, 30)
    then If $this.health is less than 1, (
        set-status($this, "dead")
    );

$result.health;
$result.status;
'''

try:
    parser = Parser(code)
    ast = parser.parse()
    env = _env.copy()  # Create a copy of the global environment

    result = eval_ast(ast, env=env)
    print("Final result:", result)

    print("\nFinal result state:")
    result_obj = env.get("result", {"health": "NOT_FOUND"})
    if isinstance(result_obj, dict):
        print("Health:", result_obj.get("health", "NOT_FOUND"))
        print("Status:", result_obj.get("status", "NOT_FOUND"))
    else:
        print("Result:", result_obj)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
