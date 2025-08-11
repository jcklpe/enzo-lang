#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.tokenizer import Tokenizer
from enzo_parser.parser import parse_program
from evaluator import eval_ast

# Test the specific conditional pipelining code
test_code = '''
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

$goblinoid
  then take-damage1($this, 30)
    then If $this.health is less than 1, (
        set-status($this, "dead")
    )
  :> $goblinoid;

$goblinoid.health;  // should print 0
$goblinoid.status;  // should print "dead"

//= IF CONDITION WITH NESTED LIST INDEX ACCESS
$nested-list: [["zero", "one"], ["two", "three"]];
'''

print("=== TOKENIZING ===")
tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()
comment_found = False
for i, token in enumerate(tokens):
    if token.type == 'COMMENT':
        print(f"{i}: {token}")
        comment_found = True
    elif 'NESTED' in str(token.value) or 'INDEX' in str(token.value):
        print(f"{i}: {token}")

if not comment_found:
    print("No COMMENT tokens found!")
    print("Looking for comment patterns in source:")
    lines = test_code.split('\n')
    for i, line in enumerate(lines):
        if '//' in line:
            print(f"Line {i}: {line}")

print("=== PARSING ===")
try:
    ast = parse_program(test_code)
    print(f"AST nodes: {len(ast.statements)}")

    print("\n=== EVALUATING ===")
    result = eval_ast(ast)
    print(f"Result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()