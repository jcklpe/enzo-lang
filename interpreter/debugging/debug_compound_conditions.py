import sys
sys.path.append('..')
from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env, _initialize_builtin_variants

# Reset environment
_env.clear()
_initialize_builtin_variants()

test_code = 'If $age is at least 18 and at most 65, ("working age");'

print("=== TOKENIZATION ===")
tokenizer = Tokenizer(test_code)
tokens = tokenizer.tokenize()
for i, token in enumerate(tokens):
    print(f"{i}: {token}")

print("\n=== PARSING ===")
try:
    ast = parse(test_code)
    print(f"Parse successful: {ast}")
except Exception as e:
    print(f"Parse failed: {e}")
    import traceback
    traceback.print_exc()
