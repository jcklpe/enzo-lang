#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

def test_case(name, code, expected):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    _env.clear()
    _initialize_builtin_variants()

    try:
        ast = parse(code)
        result = eval_ast(ast)

        # Extract results (could be a list from Program)
        if isinstance(result, list):
            results = [r for r in result if r is not None]
        else:
            results = [result] if result is not None else []

        print(f"Results: {results}")
        print(f"Expected: {expected}")

        if results == expected:
            print("✓ PASS")
        else:
            print("✖ FAIL")

    except Exception as e:
        print(f"✖ ERROR: {e}")
        import traceback
        traceback.print_exc()

# Test 1: Looping over a reference
test_case(
    "LOOPING OVER A REFERENCE TO A LIST",
    """
$original-list-ref: ["x", "y", "z"];
$ref-to-list: @original-list-ref;
$visited-ref-list: [];
Loop for $item in $ref-to-list, (
    [<$visited-ref-list>, $item] :> $visited-ref-list;
);
$visited-ref-list;
""",
    [["x", "y", "z"]]
)

# Test 2: Passing by value (copy) - default behavior
test_case(
    "PASSING BY VALUE (COPY) - DEFAULT BEHAVIOR",
    """
$original-copy: [1, 2, 3];

modify-copy: (
    param $list: ;
    $list.1 <: 99;
    $list;
);

modify-copy($original-copy);
$original-copy;
""",
    [[99, 2, 3], [1, 2, 3]]
)

# Test 3: Passing by reference
test_case(
    "PASSING BY REFERENCE - EXPLICIT WITH @",
    """
$original-ref: [1, 2, 3];

modify-reference: (
    param $list: ;
    $list.1 <: 99;
    $list;
);

modify-reference(@original-ref);
$original-ref;
""",
    [[99, 2, 3], [99, 2, 3]]
)
