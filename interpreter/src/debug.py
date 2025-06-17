#!/usr/bin/env python3
from src.parser import parse

src = """
(
$x: 100;
$y: 100;
return($x + $y);
)
""".lstrip()

ast = parse(src)
print(repr(ast))
