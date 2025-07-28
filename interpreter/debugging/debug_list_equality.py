import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, EnzoList
from src.runtime_helpers import format_val

# Test list equality comparison
code = """
$list1: [1,2,3];
$list2: [1,2,3];
$list3: [3,2,1];

If $list1 is $list2,
  "Lists are equal";
end;

If $list1 is $list3,
  "Lists are equal";
Else,
  "Lists are different";
end;

If $list1 is [1,2,3],
  "List equals literal";
end;
"""

print("Code:")
print(code)
print("\nEvaluating:")

try:
    result = eval_ast(parse(code), value_demand=True)
    print(f"Result: {result}")
    if result is not None:
        print(f"Formatted: {format_val(result)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test EnzoList equality directly
print("\nDirect EnzoList equality test:")
list1 = EnzoList()
list1.append(1)
list1.append(2)
list1.append(3)

list2 = EnzoList()
list2.append(1)
list2.append(2)
list2.append(3)

list3 = [1, 2, 3]

print(f"EnzoList([1,2,3]) == EnzoList([1,2,3]): {list1 == list2}")
print(f"EnzoList([1,2,3]) == [1,2,3]: {list1 == list3}")
print(f"[1,2,3] == EnzoList([1,2,3]): {list3 == list1}")
