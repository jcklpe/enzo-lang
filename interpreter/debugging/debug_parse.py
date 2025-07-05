#!/usr/bin/env python3

import sys
sys.path.insert(0, 'src')
from cli import split_statements
from src.enzo_parser.parser import parse
from src.evaluator import eval_ast

with open('simple_test.enzo') as f:
    lines = f.readlines()

stmts = split_statements(lines)
print('Split statements:')
for i, stmt in enumerate(stmts):
    print(f'{i}: {stmt}')

print('\nProcessing each statement:')
for i, stmt_lines in enumerate(stmts):
    statement = '\n'.join(stmt_lines).strip()
    print(f'\nStatement {i}: {statement!r}')

    try:
        print('  Parsing...')
        ast = parse(statement)
        print(f'  Parsed successfully: {ast}')

        print('  Evaluating...')
        result = eval_ast(ast, value_demand=True)
        print(f'  Result: {result}')

    except Exception as e:
        print(f'  Error: {e}')
        import traceback
        traceback.print_exc()
