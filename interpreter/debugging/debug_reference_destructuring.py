#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.evaluator import eval_ast
from src.enzo_parser.parser import parse_program

# Test reference destructuring scenario
test_code = '''
$person8: [$name8: "Dana", $age8: 50];
@person8[] :> $name8, $age8;
"Dan" :> $name8;
51 :> $age8;
$person8.name8;
$person8.age8;
'''

try:
    ast = parse_program(test_code)
    print("AST:", ast)
    result = eval_ast(ast)
    print("Result:", result)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
