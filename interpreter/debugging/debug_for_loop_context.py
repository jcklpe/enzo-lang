#!/usr/bin/env python3

from src.enzo_parser.parser import Parser

# Test the exact For loop from the test file in full context
code = '''//= SIMPLE FOR LOOP
$list-for: [1,2,3];
For $item in $list-for,
  "Item: <$item>"; // prints each item
end;'''

print("=== DEBUGGING FOR LOOP IN FULL CONTEXT ===")
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

except Exception as e:
    print(f"❌ Parse error: {e}")
    print(f"Current position: {parser.pos}")
    if parser.pos < len(parser.tokens):
        print(f"Current token: {parser.tokens[parser.pos]}")
    else:
        print("At end of tokens")

    # Print some context
    start = max(0, parser.pos - 5)
    end = min(len(parser.tokens), parser.pos + 5)
    print(f"Context tokens [{start}:{end}]:")
    for i in range(start, end):
        marker = " >>> " if i == parser.pos else "     "
        if i < len(parser.tokens):
            print(f"{marker}{i}: {parser.tokens[i]}")
        else:
            print(f"{marker}{i}: <END>")
