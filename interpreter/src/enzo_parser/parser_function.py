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

    params = []
    local_vars = []
    body = []

    # Parse bindings (KEYNAME: ...) at the start
    while True:
        t = parser.peek()
        t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
        # Only treat as binding if KEYNAME followed by BIND
        if t and t.type == "KEYNAME" and t2 and t2.type == "BIND":
            name = parser.advance().value
            parser.advance()  # consume BIND
            # Support empty bind: $x: ;
            if parser.peek() and parser.peek().type in ("SEMICOLON", "COMMA", "RPAR"):
                local_vars.append(Binding(name, None))
            else:
                value = parser.parse_value_expression()
                local_vars.append(Binding(name, value))
            # Accept and consume all consecutive semicolons or commas after a binding
            while parser.peek() and parser.peek().type in ("SEMICOLON", "COMMA"):
                parser.advance()
            continue
        break

    # After bindings, parse the body (expressions/statements) until RPAR
    while parser.peek() and parser.peek().type not in ("RPAR",):
        expr = parser.parse_value_expression()
        body.append(expr)
        # Accept and consume all consecutive semicolons or commas after a statement
        while parser.peek() and parser.peek().type in ("SEMICOLON", "COMMA"):
            parser.advance()

    parser.expect("RPAR")
    ast = FunctionAtom([], local_vars, body)
    log_debug(f"[parse_function_atom] AST: {ast}")
    log_debug(f"[parse_function_atom] tokens after: {parser.tokens[parser.pos:]}")
    return ast
