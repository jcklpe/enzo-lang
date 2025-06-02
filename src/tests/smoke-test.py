from enzo.exec import eval_ast
from enzo.parser import parse

def run(src: str):
    return eval_ast(parse(src))

def test_basic():
    assert run('"hello"') == "hello"
    assert run('$x: 2') == 2
    run('$x: 2')  # define
    assert run('"num is < $x >"') == "num is 2"
    run('$list: [\"a\",\"b\",\"c\"]')
    run('$i: 3')
    assert run('"pick < $list.$i >"') == "pick c"
