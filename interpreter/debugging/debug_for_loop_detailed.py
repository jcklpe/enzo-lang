#!/usr/bin/env python3

from src.enzo_parser.parser import Parser

# Test the exact For loop from the test file
code = '''$list-for: [1,2,3];
For $item in $list-for,
  "Item: <$item>";
end;'''

print("=== DEBUGGING FOR LOOP PARSING ===")
print(f"Code:\n{code}")
print()

parser = Parser(code)
print("Tokens:")
for i, token in enumerate(parser.tokens):
    print(f"  {i}: {token}")
print()

try:
    ast = parser.parse()
    print("✅ Parsed successfully!")
    print(f"AST: {ast}")

    # Try to evaluate it
    from src.evaluator import eval_ast
    print("\n=== EVALUATION ===")

    # Initialize environment
    env = {}

    # Evaluate each statement
    results = []
    for stmt in ast:
        result = eval_ast(stmt, env=env)
        if result is not None:
            results.append(result)
            print(f"Statement result: {result}")

    print(f"Final results: {results}")

except Exception as e:
    print(f"❌ Parse error: {e}")
    print(f"Current position: {parser.pos}")
    if parser.pos < len(parser.tokens):
        print(f"Current token: {parser.tokens[parser.pos]}")
    else:
        print("At end of tokens")

    # Print some context
    start = max(0, parser.pos - 3)
    end = min(len(parser.tokens), parser.pos + 3)
    print(f"Context tokens [{start}:{end}]:")
    for i in range(start, end):
        marker = " >>> " if i == parser.pos else "     "
        if i < len(parser.tokens):
            print(f"{marker}{i}: {parser.tokens[i]}")
        else:
            print(f"{marker}{i}: <END>")
