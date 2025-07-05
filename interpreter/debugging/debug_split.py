#!/usr/bin/env python3

import sys
sys.path.insert(0, 'src')
from cli import split_statements

with open('simple_test.enzo') as f:
    lines = f.readlines()

print('Input lines:')
for i, line in enumerate(lines):
    print(f'{i}: {line!r}')

stmts = split_statements(lines)
print('\nSplit statements:')
for i, stmt in enumerate(stmts):
    print(f'{i}: {stmt}')
