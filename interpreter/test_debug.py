#!/usr/bin/env python3

import sys
sys.path.append('src')

from enzo_parser.parser import parse_program
from runtime_helpers import log_debug

# Test the working cases first
test_cases = [
    """($z: 101;
$t: 101;
return(($z + $t))
)""",
    """($z: 101;
$t: 102;
return(($z + $t));
)"""
]

for i, case in enumerate(test_cases):
    print(f"\n=== Test Case {i+1} ===")
    print(f"Code: {repr(case)}")
    try:
        ast = parse_program(case)
        print(f"Success: {ast}")
    except Exception as e:
        print(f"Error: {e}")
