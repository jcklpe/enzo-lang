from .ast_nodes import FunctionAtom, Binding
from .parser_utilities import expect

def parse_function_atom(parser):
    expect(parser, "LPAR")
    t = parser.peek()
    if t and t.type == "RPAR":
        parser.advance()
        return FunctionAtom([], [], [], code_line=parser._get_code_line(t))
    t = parser.peek()
    if t and t.type == "KEYNAME":
        save_pos = parser.pos
        name = t.value
        parser.advance()
        if parser.peek() and parser.peek().type == "COLON":
            parser.pos = save_pos
            items = []
            sep_seen = False
            while parser.peek() and not (parser.peek().type == "RPAR"):
                t = parser.peek()
                if t.type == "KEYNAME":
                    name = parser.advance().value
                    if parser.peek() and parser.peek().type == "COLON":
                        parser.advance()
                        if parser.peek() and not (parser.peek().type in ("COMMA", "SEMICOLON", "RPAR")):
                            value_expression = parser.parse_value_expression()
                            items.append(Binding(name, value_expression))
                        else:
                            items.append(Binding(name, None))
                    else:
                        items.append(name)
                else:
                    items.append(parser.parse_value_expression())
                if parser.peek() and parser.peek().type in ("COMMA", "SEMICOLON"):
                    sep_seen = True
                    parser.advance()
            parser.expect("RPAR")
            params = []
            local_vars = []
            body = []
            for item in items:
                if isinstance(item, Binding) and item.value is None:
                    params.append(item.name)
                elif isinstance(item, Binding):
                    local_vars.append(item)
                else:
                    body.append(item)
            return FunctionAtom(params, local_vars, body)
        else:
            parser.pos = save_pos
    expr = parser.parse_value_expression()
    parser.expect("RPAR")
    return FunctionAtom([], [], [expr])
