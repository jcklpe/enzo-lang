# Debug parser
import sys
sys.path.insert(0, 'src')

from src.enzo_parser.parser import parse
from src.enzo_parser.tokenizer import Tokenizer

code = '''$status: "ready";
If $status, (
    "Ready!";
);'''

print("Parsing:", repr(code))
tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()
print("Tokens:", [(t.type, t.value) for t in tokens])

try:
    ast = parse(code)
    print("AST nodes:")
    if hasattr(ast, 'statements'):
        nodes = ast.statements
    else:
        nodes = ast  # ast is already a list

    for i, node in enumerate(nodes):
        print(f"{i}: {type(node).__name__} - {node}")
except Exception as e:
    print("Parse error:", e)
    import traceback
    traceback.print_exc()
