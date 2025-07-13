#!/usr/bin/env python3

from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast

# Test the exact failing case from the tests
code = '''
Animal: <[
    position: [Number, Number, Number],
]>;

Flying-Animal: <[
    wings: "true",
    fly: (
        param $z-position-movement: Number;
        $self.position.3 + $z-position-movement :> $self.position.3;
        return($self);
    )
]>;

Duck: Animal and Flying-Animal;

$donald: Duck[
    $position: [10, 5, 0]
];
$donald.position;
$donald.fly(5);
$donald.position.3;
'''

ast = parse_program(code)
env = {
    'Number': 'Number',
    'Text': 'Text',
    '$self': '$self'
}

for stmt in ast.statements:
    try:
        result = eval_ast(stmt, env=env)
        print(f'Result: {result}')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
