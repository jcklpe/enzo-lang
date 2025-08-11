#!/usr/bin/env python3

# Test the exact sequence that causes the issue
test_content = '''//= INLINE IF TRUE and FALSE
$inline-if: "ready";
If $inline-if, "Go!"; end; // prints "Go!"
$inline-if<: "";
If $inline-if, "Go!"; Else, "Wait!"; end; // prints "Wait!"

//= SIMPLE FOR LOOP
$list-for: [1,2,3];
For $item in $list-for,
  "Item: <$item>"; // prints each item
end;

//= WHILE LOOP SIMPLE
$count-while: 1;
While $count-while is less than 3,
  $count-while;
  $count-while <: $count-while + 1;
end;
$count-while; // prints 3'''

print("=== TESTING SEQUENCE THAT CAUSES FAILURE ===")

from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast

try:
    print("Parsing...")
    ast = parse_program(test_content)
    print("✅ Parsed successfully!")
    print("Evaluating...")
    result = eval_ast(ast, value_demand=True)
    print("✅ Evaluated successfully!")
    print(f"Results: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
