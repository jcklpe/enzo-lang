#!/usr/bin/env python3

import sys
sys.path.append('/Users/aslan/work/enzo-lang/interpreter/src')

from enzo_parser.parser import Parser
from evaluator import eval_ast, _env

# Test the exact pipeline from the test case
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

$pipeline_result: $goblinoid
  then take-damage1($this, 30)
    then If $this.health is less than 1, (
        set-status($this, "dead")
    );

"Pipeline result:";
$pipeline_result;
"Pipeline result health:";
$pipeline_result.health;
"Pipeline result status:";
$pipeline_result.status;

$pipeline_result :> $goblinoid;

"After rebind:";
$goblinoid.health;
$goblinoid.status;
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
