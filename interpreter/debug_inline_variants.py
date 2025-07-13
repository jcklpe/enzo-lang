#!/usr/bin/env python3

from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast

# Test variant group with inline blueprints
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
'''

env = {
    'Number': 'Number',
    'Text': 'Text',
    '$self': '$self'
}

try:
    ast = parse_program(code)
    print("AST parsed successfully")

    for stmt in ast.statements:
        try:
            result = eval_ast(stmt, env=env)
            if result is not None:
                print(f"Result: {result}")
        except Exception as e:
            print(f"Evaluation error: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()
