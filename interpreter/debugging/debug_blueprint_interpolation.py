#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast, _env

# Test the blueprint interpolation case that's failing
code = '''
BP-example: <[foo: Number]>;
$bp1: BP-example[$foo: 10];
$li31: [<$bp1>];
'''

print("=== DEBUGGING BLUEPRINT INTERPOLATION ===")
print(f"Code:\n{code}")

try:
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    print(f"\nTokens: {[str(t) for t in tokens]}")

    parser = Parser(code)
    ast = parser.parse()
    print(f"\nAST: {ast}")

    result = eval_ast(ast, env=_env)
    print(f"\nResult: {result}")

    # Let's specifically check what $bp1 evaluates to
    from src.enzo_parser.ast_nodes import VarInvoke
    bp1_var = VarInvoke(name='$bp1')
    bp1_value = eval_ast(bp1_var, value_demand=True, env=_env)
    print(f"\n$bp1 evaluates to: {bp1_value}")
    print(f"$bp1 type: {type(bp1_value)}")
    print(f"Is EnzoList: {hasattr(bp1_value, '_elements')}")

except Exception as e:
    print(f"\nException: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()