#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.evaluator import eval_ast
from src.enzo_parser.parser import parse_program

# Test restructuring scenario
test_code = '''
$person7: [$name7: "Bea", $age7: 40];
$name7, $age7: $person7[];
"Beatrix" :> $name7;
$age7<: 41;
$name7;
$age7;
$person7[] <: [$name7, $age7];
$person7.name7;
$person7.age7;
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
