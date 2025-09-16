import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

test_code = '''
rec_factorial: (
    param $n: ;
    "Debug: factorial called with <$n>";
    If $n is at most 1, (
        "Debug: base case, returning 1";
        return(1);
    );
    "Debug: recursive case for <$n>";
    $result: $n * rec_factorial($n - 1);
    "Debug: got result <$result> for <$n>";
    return($result);
);

"Starting factorial(3)";
rec_factorial(3);
'''

ast = parse(test_code)
result = eval_ast(ast)