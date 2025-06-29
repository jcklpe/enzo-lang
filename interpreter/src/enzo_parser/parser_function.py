from .ast_nodes import FunctionAtom, Binding, VarInvoke
from .parser_utilities import expect

import os

def log_debug(msg):
    log_path = os.path.join(os.path.dirname(__file__), "../logs/debug.log")
    with open(log_path, "a") as f:
        f.write(msg + "\n")

def parse_function_atom(parser):
    # Log tokens before parsing
    log_debug(f"[parse_function_atom] tokens before: {parser.tokens[parser.pos:]}")
    expect(parser, "LPAR")
    t = parser.peek()
    if t and t.type == "RPAR":
        parser.advance()
        ast = FunctionAtom([], [], [], code_line=parser._get_code_line(t))
        log_debug(f"[parse_function_atom] AST: {ast}")
        log_debug(f"[parse_function_atom] tokens after: {parser.tokens[parser.pos:]}")
        return ast
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
                        items.append(VarInvoke(name, code_line=parser._get_code_line(t)))
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
            ast = FunctionAtom(params, local_vars, body)
            log_debug(f"[parse_function_atom] AST: {ast}")
            log_debug(f"[parse_function_atom] tokens after: {parser.tokens[parser.pos:]}")
            return ast
        else:
            parser.pos = save_pos
    # --- FIX: Parse a block of statements for the function body ---
    body = parser.parse_block()
    parser.expect("RPAR")
    # parse_block may return a single node or a list; always store as a list
    if not isinstance(body, list):
        body = [body]
    ast = FunctionAtom([], [], body)
    log_debug(f"[parse_function_atom] AST: {ast}")
    log_debug(f"[parse_function_atom] tokens after: {parser.tokens[parser.pos:]}")
    return ast
