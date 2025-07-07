from src.enzo_parser.ast_nodes import FunctionAtom, Binding, VarInvoke
from src.enzo_parser.parser_utilities import expect
from src.runtime_helpers import log_debug
from src.error_handling import EnzoParseError

import os

def synchronize(parser):
    # Skip tokens until we reach a likely statement boundary: SEMICOLON, COMMA, RPAR, RBRACK, RBRACE, or EOF
    while parser.peek() and parser.peek().type not in ("SEMICOLON", "COMMA", "RPAR", "RBRACK", "RBRACE"):
        parser.advance()
    # Optionally, advance past the boundary token
    if parser.peek():
        parser.advance()

def parse_function_atom(parser):
    from src.error_handling import EnzoParseError
    from src.runtime_helpers import log_debug
    lpar_token = parser.peek()
    log_debug(f"[parse_function_atom] ENTER pos={parser.pos}, token={lpar_token}")
    expect(parser, "LPAR")
    lpar_line = None
    if lpar_token:
        lpar_line = parser.src[:lpar_token.start].count('\n') + 1

    params = []  # Store (name, default_value) tuples
    local_vars = []
    body = []

    # Parse the body statements directly with the main parser
    while parser.peek() and parser.peek().type != "RPAR":
        log_debug(f"[parse_function_atom] parsing statement at token: {parser.peek()} (parser.pos={parser.pos})")
        stmt = parser.parse_statement()
        from src.enzo_parser.ast_nodes import Binding, ParameterDeclaration
        if isinstance(stmt, Binding):
            local_vars.append(stmt)
        elif isinstance(stmt, ParameterDeclaration):
            # Convert parameter declaration to the format expected by FunctionAtom
            params.append((stmt.name, stmt.default_value))
        else:
            body.append(stmt)
        # Always consume all delimiters after every statement, including after return
        while parser.peek() and parser.peek().type in ("SEMICOLON", "COMMA"):
            parser.advance()
            log_debug(f"[parse_function_atom] skipped delimiter, now at parser.pos={parser.pos}")

    # Expect the closing RPAR
    if parser.peek() and parser.peek().type == "RPAR":
        rpar_token = parser.peek()
        parser.advance()  # consume the RPAR
        log_debug(f"[parse_function_atom] consumed closing RPAR at parser.pos={parser.pos-1}")

        rpar_line = parser.src[:rpar_token.start].count('\n') + 1
        log_debug(f"[parse_function_atom] lpar_line={lpar_line}, rpar_line={rpar_line}")
        is_multiline = lpar_line is not None and rpar_line is not None and lpar_line != rpar_line
        log_debug(f"[parse_function_atom] is_multiline={is_multiline}")
    else:
        log_debug(f"[parse_function_atom] ERROR: expected RPAR but found {parser.peek()}")
        from src.error_messaging import error_message_unmatched_parenthesis
        raise EnzoParseError(error_message_unmatched_parenthesis())

    # Only consume trailing semicolons, NOT commas (commas belong to parent context like lists)
    while parser.peek() and parser.peek().type == "SEMICOLON":
        log_debug(f"[parse_function_atom] skipping trailing semicolon after function atom at parser.pos={parser.pos}")
        parser.advance()

    ast = FunctionAtom(params, local_vars, body, code_line=parser._get_code_line(lpar_token), is_multiline=is_multiline)
    log_debug(f"[parse_function_atom] AST: {ast}")
    log_debug(f"[parse_function_atom] EXIT parser.pos={parser.pos}, next token={parser.peek()}")
    return ast
