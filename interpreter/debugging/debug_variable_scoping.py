import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_scoping_case(name, code):
    print(f"\n=== {name} ===")
    print(f"Code: {code}")
    try:
        _env.clear()
        _initialize_builtin_variants()
        ast = parse(code)
        result = eval_ast(ast, value_demand=True)
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

print("=== VARIABLE SCOPING DEBUG ===")

# Test 1: Loop with rebinding in global scope (should work)
test_scoping_case("Global scope loop",
    "$total: 0; $numbers: [1, 2, 3]; Loop for $num in $numbers, ($total + $num :> $total;); $total;")

# Test 2: Loop with rebinding in function scope (likely fails)
test_scoping_case("Function scope loop",
    "test_func: ($total: 0; $numbers: [1, 2, 3]; Loop for $num in $numbers, ($total + $num :> $total;); return($total);); test_func();")

# Test 3: Simple variable access in function (should work)
test_scoping_case("Function variable access",
    "test_func: ($x: 5; return($x);); test_func();")

# Test 4: Simple rebinding in function (should work)
test_scoping_case("Function variable rebind",
    "test_func: ($x: 5; 10 :> $x; return($x);); test_func();")

# Test 5: Loop without rebinding in function (might work)
test_scoping_case("Function loop without rebind",
    "test_func: ($numbers: [1, 2, 3]; Loop for $num in $numbers, ($num;); return(\"done\");); test_func();")

# Test 6: Count in loop
test_scoping_case("Function count in loop",
    "test_func: ($count: 0; $numbers: [1, 2, 3]; Loop for $num in $numbers, ($count + 1 :> $count;); return($count);); test_func();")
