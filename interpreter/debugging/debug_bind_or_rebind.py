#!/usr/bin/env python3
"""Debug BindOrRebind specifically"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

# Monkey patch BindOrRebind to add debugging
original_eval_ast = eval_ast

def debug_eval_ast(node, env=None, **kwargs):
    from src.enzo_parser.ast_nodes import BindOrRebind, VarInvoke

    if isinstance(node, BindOrRebind):
        target_name = node.target if isinstance(node.target, str) else (node.target.name if isinstance(node.target, VarInvoke) else str(node.target))
        if target_name == '$active-while':
            print(f"DEBUG BindOrRebind: target={target_name}")
            print(f"  env keys: {list(env.keys()) if env else 'None'}")
            print(f"  outer_env: {kwargs.get('outer_env', 'None')}")
            print(f"  outer_env keys: {list(kwargs.get('outer_env', {}).keys()) if kwargs.get('outer_env') else 'None'}")
            print(f"  loop_locals: {kwargs.get('loop_locals', 'None')}")
            print(f"  value will be: {kwargs}")

    return original_eval_ast(node, env, **kwargs)

# Apply the monkey patch
import src.evaluator
src.evaluator.eval_ast = debug_eval_ast

test_code = '''
$active-while: True;
$counter-while: 4;
$counter-while + 1 :> $counter-while;
If $counter-while is 5, (
    False :> $active-while;
);
$active-while;
'''

print("Testing BindOrRebind debugging...")
print("=" * 50)

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
    print(f"Environment: active={_env.get('$active-while')}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
