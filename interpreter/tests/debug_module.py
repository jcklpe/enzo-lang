# import ast
# import sys

# from src.evaluator import eval_ast, EnzoRuntimeError
# from src.error_handling import EnzoParseError
# from src.enzo_parser.parser import parse_program


# def is_effectively_empty(filename):
#     with open(filename, 'r') as f:
#         source = f.read()
#     try:
#         tree = ast.parse(source, filename=filename)
#     except Exception:
#         return False  # If it can't parse, treat as not empty
#     for node in tree.body:
#         if not isinstance(node, (ast.Import, ast.ImportFrom, ast.Expr)):
#             return False
#         if isinstance(node, ast.Expr):
#             # Only allow docstrings (string expressions)
#             if not isinstance(node.value, ast.Str):
#                 return False
#     return True


# def print_ast_debug(src, label=None):
#     # Print AST and evaluation diagnostics for the given Enzo source string.
#     # Optionally provide a label for context (e.g., test name or file).
#     print("="*60)
#     if label:
#         print(f"[debug-module.py] Diagnostics for: {label}\n")
#     try:
#         program_ast = parse_program(src)
#         print("AST (Program):\n", program_ast)
#         print("\n--- Individual Statements ---")
#         for i, stmt in enumerate(program_ast.statements):
#             print(f"\nStatement {i+1} AST: {stmt!r}")
#         print("\n--- Evaluation Output ---")
#         result = eval_ast(program_ast)
#         print("Result:", result)
#     except (EnzoParseError, EnzoRuntimeError, Exception) as e:
#         print("Exception during parse/eval:", e)
#     print("="*60)
#     print("[debug-module.py] End of debug output.\n")


# if __name__ == "__main__":
#     if is_effectively_empty(__file__):
#         sys.exit(0)
#     import sys
#     print("="*60)
#     print("[debug-module.py] Standalone debug mode\n")
#     if len(sys.argv) > 1:
#         src = sys.argv[1]
#     else:
#         # Default: minimal test case for :> bug
#         src = "55 :> $newImplicit;"
#     print(f"Source code to debug:\n{src}\n")
#     print_ast_debug(src, label="Standalone run")