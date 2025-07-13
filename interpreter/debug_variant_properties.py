#!/usr/bin/env python3

from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast

# Test variant instance property access
code = '''
Monster3 variants:
    Monster3: <[
        health: Number,
        position: [Number, Number]
   ]>,
    and Goblin3: <[
        cackle: (
            return("heeheehee");
        )
   ]>;

$g: Monster3.Goblin3[$health: 7, $position: [8,8]];
$g.cackle();
$g.health;
'''

env = {
    'Number': 'Number',
    'Text': 'Text',
    '$self': '$self'
}

try:
    ast = parse_program(code)
    print("AST parsed successfully")

    for i, stmt in enumerate(ast.statements):
        try:
            result = eval_ast(stmt, env=env)
            print(f"Statement {i}: {type(stmt).__name__}")
            if result is not None:
                print(f"  Result: {result}")

            # Always print environment state after each statement
            print(f"  Environment keys: {[k for k in env.keys() if not k.startswith('$') or k in ['$self']]}")
            if 'Monster3' in env:
                print(f"  Monster3 type: {type(env['Monster3'])}")
                if hasattr(env['Monster3'], 'fields'):
                    print(f"  Monster3 fields: {env['Monster3'].fields}")
            if 'Goblin3' in env:
                print(f"  Goblin3 type: {type(env['Goblin3'])}")
                if hasattr(env['Goblin3'], 'fields'):
                    print(f"  Goblin3 fields: {env['Goblin3'].fields}")
            print()
        except Exception as e:
            print(f"Evaluation error: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()
