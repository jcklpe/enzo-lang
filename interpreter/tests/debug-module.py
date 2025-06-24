from src.parser import parse
from src.evaluator import eval_ast, InterpolationParseError

test_cases = [
    # Multi-line anonymous, no explicit return
    "($x: 1;\n $y: 2;\n $x + $y;\n);",
    # Multi-line with explicit return
    "(\n$x: 100;\n$y: 100;\nreturn(($x + $y));\n);",
    # Param + default values, multi-line
    "adder: (\nparam $x: 6;\nparam $y: 6;\nreturn(($y + $x));\n); adder(); $adder(); $adder;",
]

for src in test_cases:
    print("="*60)
    print("Source:", src)
    try:
        ast = parse(src)
        print("AST:", ast)
        result = eval_ast(ast)
        print("Result:", result)
    except Exception as e:
        print("Exception during eval:", e)
print("="*60)
print("[debug-module.py] End of debug output.\n")