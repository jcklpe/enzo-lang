import sys
sys.path.insert(0, '.')

from src.enzo_parser.parser import parse

# Test parsing just the variable binding
code = "$test-var: 42;"
ast = parse(code)
print(f"Variable binding AST: {ast}")
print(f"AST type: {type(ast)}")

# Test parsing just the variable invocation
code2 = "$test-var;"
ast2 = parse(code2)
print(f"Variable invocation AST: {ast2}")
print(f"AST type: {type(ast2)}")

# Test parsing both together (not in if statement)
code3 = "$test-var: 42; $test-var;"
ast3 = parse(code3)
print(f"Both statements AST: {ast3}")
print(f"AST type: {type(ast3)}")
if isinstance(ast3, list):
    print(f"Number of statements: {len(ast3)}")
    for i, stmt in enumerate(ast3):
        print(f"Statement {i}: {stmt} (type: {type(stmt)})")
