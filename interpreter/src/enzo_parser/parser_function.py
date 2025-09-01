from src.enzo_parser.ast_nodes import FunctionAtom, Binding, VarInvoke
from src.enzo_parser.parser_utilities import expect
from src.runtime_helpers import log_debug
from src.error_handling import EnzoParseError
from src.error_messaging import error_message_duplicate_param

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
    param_names = set()  # Track parameter names for duplicates

    try:
        # Parse the body statements directly with the main parser
        while parser.peek() and parser.peek().type != "RPAR":
            log_debug(f"[parse_function_atom] parsing statement at token: {parser.peek()} (parser.pos={parser.pos})")
            stmt = parser.parse_statement()
            from src.enzo_parser.ast_nodes import Binding, ParameterDeclaration
            if isinstance(stmt, ParameterDeclaration):
                # Duplicate parameter name detection (raise error before any output or AST modification)
                if stmt.name in param_names:
                    # Find the actual line containing the duplicate parameter
                    # Look for the line that contains "param <n>:" where name matches stmt.name
                    # We want the SECOND occurrence since that's the duplicate
                    src_lines = parser.src.splitlines()
                    code_line = None
                    # stmt.name should already include the $ prefix
                    target_pattern = f"param {stmt.name}:"
                    occurrences = []
                    for line in src_lines:
                        if target_pattern in line:
                            # Strip comments from the line
                            line_without_comment = line.split('//')[0].strip()
                            occurrences.append(line_without_comment)
                    # Use the second occurrence if available, otherwise first
                    if len(occurrences) >= 2:
                        code_line = occurrences[1]  # Second occurrence (the duplicate)
                    elif len(occurrences) >= 1:
                        code_line = occurrences[0]  # Fallback to first occurrence
                    else:
                        code_line = f"param {stmt.name};"  # fallback
                    msg = error_message_duplicate_param(stmt.name, code_line)
                    raise EnzoParseError(msg, code_line=code_line)
                    # Ensure no further code is executed after the error
                    return  # (unreachable, for clarity)
                # Only add to param_names and params if not duplicate
                param_names.add(stmt.name)
                params.append((stmt.name, stmt.default_value))
            elif isinstance(stmt, Binding):
                # Variable bindings should be part of the function body AND tracked as local vars
                local_vars.append(stmt)
                body.append(stmt)
            else:
                body.append(stmt)
            # Always consume all delimiters after every statement, including after return
            while parser.peek() and parser.peek().type in ("SEMICOLON", "COMMA"):
                parser.advance()
                log_debug(f"[parse_function_atom] skipped delimiter, now at parser.pos={parser.pos}")
    except EnzoParseError as e:
        # Only wrap errors that don't already have meaningful error messages
        # Let specific validation errors (duplicate params, $this declarations, etc.) pass through
        if e.args[0].startswith("error: "):
            # This is already a well-formatted error message, don't wrap it
            raise e
        else:
            # This is a generic parsing error, wrap it with function context
            synchronize(parser)  # Skip to the end of the function atom after generic errors
            raise EnzoParseError("error: parse error in Function atom body", code_line=e.code_line)

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
