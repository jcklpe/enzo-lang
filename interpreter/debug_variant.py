#!/usr/bin/env python3

from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast

# Test simple variant instantiation
code = '''
Goblin1: <[
    health: Number,
    position: [Number, Number],
    cackle: (
        return("heeheehee");
    )
]>;
Monster1 variants: Goblin1;
$enemy1: Monster1.Goblin1[$health: 25, $position: [1,1]];
$enemy1.cackle();
'''

env = {
    'Number': 'Number',
    'Text': 'Text',
    '$self': '$self'
}

try:
    ast = parse_program(code)
    print("AST parsed successfully")
    print("Last statement AST:", ast.statements[-1])

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
