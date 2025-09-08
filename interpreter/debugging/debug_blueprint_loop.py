import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_case(name, code):
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
        import traceback
        traceback.print_exc()
        return None

print("=== DEBUGGING BLUEPRINT METHOD LOOP ISSUE ===")

# Test 1: Minimal case - basic loop
test_case("Basic loop outside function", """
$total: 0;
$numbers: [1, 2, 3];
Loop for $num in $numbers, (
    $total + $num :> $total;
);
$total;
""")

# Test 2: Loop in regular function
test_case("Loop in regular function", """
test_func: (
    $total: 0;
    $numbers: [1, 2, 3];
    Loop for $num in $numbers, (
        $total + $num :> $total;
    );
    return($total);
);
test_func();
""")

# Test 3: Blueprint method accessing field
test_case("Blueprint method accessing field", """
Test: <[
    numbers: [1, 2, 3],
    get_numbers: (
        return($self.numbers);
    )
]>;
$t: Test[];
$t.get_numbers();
""")

# Test 4: Blueprint method with simple loop (no field access)
test_case("Blueprint method with simple loop", """
Test: <[
    sum_simple: (
        $total: 0;
        $numbers: [1, 2, 3];
        Loop for $num in $numbers, (
            $total + $num :> $total;
        );
        return($total);
    )
]>;
$t: Test[];
$t.sum_simple();
""")

# Test 5: Blueprint method with loop accessing field
test_case("Blueprint method with loop accessing field", """
Test: <[
    numbers: [1, 2, 3],
    sum_field: (
        $total: 0;
        Loop for $num in $self.numbers, (
            $total + $num :> $total;
        );
        return($total);
    )
]>;
$t: Test[];
$t.sum_field();
""")

# Test 6: The actual failing case
test_case("Actual failing case - calculate_average", """
Student: <[
    name: "Unknown",
    scores: [],
    calculate_average: (
        $total: 0;
        $count: 0;
        Loop for $score in $self.scores, (
            $total + $score :> $total;
            $count + 1 :> $count;
        );
        return($total / $count);
    )
]>;

$alice: Student[
    $name: "Alice",
    $scores: [95, 87, 92, 89]
];

$alice.calculate_average();
""")
