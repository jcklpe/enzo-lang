import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Clear and reinitialize environment
_env.clear()
_initialize_builtin_variants()

# Patch the eval_ast function to add logging for BindOrRebind operations
original_eval_ast = eval_ast

def debug_eval_ast(node, *args, **kwargs):
    from src.enzo_parser.ast_nodes import BindOrRebind, VarInvoke
    if isinstance(node, BindOrRebind):
        print(f"\n=== REBIND OPERATION ===")
        print(f"Target: {node.target}")
        print(f"Value: {node.value}")
        print(f"kwargs: {kwargs}")

        # Extract parameters
        env = kwargs.get('env')
        outer_env = kwargs.get('outer_env')
        loop_locals = kwargs.get('loop_locals')
        is_function_context = kwargs.get('is_function_context', False)

        print(f"env type: {type(env)}")
        print(f"outer_env is not None: {outer_env is not None}")
        print(f"loop_locals is not None: {loop_locals is not None}")
        print(f"is_function_context: {is_function_context}")

        if isinstance(node.target, VarInvoke):
            name = node.target.name
            print(f"Variable name: {name}")

            if outer_env is not None:
                print(f"Variable '{name}' in outer_env: {name in outer_env}")

            if loop_locals is not None:
                print(f"Variable '{name}' in loop_locals: {name in loop_locals}")

            # Check which branch will be taken
            from collections import ChainMap
            if isinstance(env, ChainMap) and len(env.maps) > 1:
                print("Branch: ChainMap handling")
                if is_function_context and name in env.maps[0]:
                    print("  -> Local shadowing")
                else:
                    found_in_closure = False
                    for i, env_layer in enumerate(env.maps[1:], 1):
                        if name in env_layer:
                            print(f"  -> Found in closure layer {i}")
                            found_in_closure = True
                            break
                    if not found_in_closure:
                        print("  -> Not found in closure layers")
            elif loop_locals is not None and name in loop_locals:
                print("Branch: Loop locals (shadowed)")
            elif outer_env is not None and name in outer_env:
                print("Branch: Outer env rebind")
            else:
                print("Branch: Current env")

        print("=== END REBIND OPERATION ===\n")

    result = original_eval_ast(node, *args, **kwargs)
    return result# Monkey patch
import src.evaluator
src.evaluator.eval_ast = debug_eval_ast

# Test case
test_code = '''
$test-var: True;
Loop, (
    If True, (
        False :> $test-var;
    );
    $test-var;
    end-loop;
);
$test-var;
'''

print("=== Test: Rebind inside If statement in loop ===")
ast = parse(test_code)
statements = ast if isinstance(ast, list) else ast.statements

for statement in statements:
    result = eval_ast(statement)

print(f"\nFinal $test-var: {_env.get('$test-var', 'NOT_FOUND')}")