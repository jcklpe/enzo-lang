# Centralized error message formatting for Enzo

def error_message_already_defined(name):
    # Only add $ if not already present
    if not name.startswith("$"):
        name = f"${name}"
    return f"error: {name} already defined"

def error_message_unknown_variable(name):
    if not name.startswith("$"):
        name = f"${name}"
    return f"unknown variable: {name}"

def error_message_not_a_function(func):
    return f"{func} is not a function"

def error_message_tuple_ast():
    return "Tuple-based ASTs are no longer supported. All nodes must be AST objects."

def error_message_unknown_node(node):
    return f"unknown node: {type(node)} {node}"

def error_message_unterminated_interpolation():
    return "unterminated interpolation in text_atom"

def error_message_included_file_not_found(fname):
    return f"included file not found: {fname}"

def error_message_generic(msg):
    return str(msg)

def error_message_expected_type(expected, got):
    return f"Expected {expected}, got {got}"

def error_message_unexpected_token(token):
    # Special case: extra semicolon
    if getattr(token, 'type', None) == 'SEMICOLON' and getattr(token, 'value', None) == ';':
        return "error: extra semicolon"
    return f"Unexpected token: {token}"

def error_message_cannot_assign(new_type, old_type):
    return f"error: cannot assign {new_type} to {old_type}"

def error_message_double_minus(token=None):
    return "error: double minus not allowed"

def error_message_list_index_out_of_range():
    return "error: list index out of range"

def error_message_cant_use_string_as_index():
    return "error: can't use string as index"

def error_message_index_applies_to_lists():
    return "error: index applies to lists"

def error_message_table_property_not_found(prop):
    return f"error: table property not found: {prop}"

def error_message_index_must_be_number():
    return "error: index must be a number (text atoms cannot be used as indices)"

def error_message_index_must_be_integer():
    return "error: index must be an integer"

def error_message_assignment_to_list_index_out_of_range():
    return "error: list index out of range"

def error_message_assignment_to_table_property_not_found(prop):
    return f"error: table property not found: {prop}"

# User-friendly error message for parse errors, with code context.
def format_parse_error(err, src=None):
    def add_context(msg):
        if src and hasattr(err, "line"):
            lines = src.splitlines()
            if 1 <= err.line <= len(lines):
                code_line = lines[err.line - 1]
                # Indent code line by 4 spaces
                msg += "\n    " + code_line.rstrip()
                # Caret underline at error column (1-based)
                if hasattr(err, "column") and err.column is not None:
                    caret_pos = max(0, err.column - 1)
                    msg += "\n" + " " * (4 + caret_pos) + "^"
        return msg

    # Special cases for commas in lists/tables
    if hasattr(err, 'token') and hasattr(err, 'expected'):
        tok = err.token
        line_txt = src.splitlines()[err.line - 1] if src and err.line <= len(src.splitlines()) else ""
        stripped = line_txt.strip().replace(" ", "")
        # Double comma: [1,,2] or {a,,b}
        if ",," in line_txt.replace(" ", ""):
            msg = "error: double comma in list"
            return add_context(msg)
        # Leading comma: [,1,2] or {,a,b}
        if stripped.startswith("[,") or stripped.startswith("{,"):
            msg = "error: excess leading comma"
            return add_context(msg)
        # Just a comma: [,] or {,}
        if stripped in ("[,]", "{,}"):
            msg = "error: empty list with just a comma"
            return add_context(msg)
        # Default: show expected tokens
        expected = ", ".join(sorted(err.expected))
        expected = expected.replace("TEXT_ATOM", "STRING")
        msg = (
            f"Syntax error: Unexpected token '{err.token}' "
            f"at line {err.line}, column {err.column}.\n"
            f"Expected one of: {expected}"
        )
        return add_context(msg)
    elif hasattr(err, 'char'):
        if err.char == "-":
            msg = "error: double minus not allowed"
        elif err.char == '"':
            msg = "error: unterminated string"
        else:
            msg = f"Syntax error: Unexpected character '{err.char}'"
        return add_context(msg)
    elif hasattr(err, 'pos_in_stream'):
        msg = f"Syntax error: Unexpected input at position {err.pos_in_stream}."
        return add_context(msg)
    else:
        msg = f"Parse error: {err}"
        return add_context(msg)
