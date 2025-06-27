# Centralized error message formatting for Enzo

def error_message_already_defined(name):
    # Only add $ if not already present
    if not name.startswith("$"):
        name = f"${name}"
    return f"{name} already defined"

def error_message_unknown_variable(name):
    return f"unknown variable: ${name}"

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
    # Special case: double semicolon
    if getattr(token, 'type', None) == 'OPERATOR' and getattr(token, 'value', None) == ';':
        return "error: extra semicolon"
    return f"Unexpected token: {token}"

# User-friendly error message for parse errors, with code context.
def format_parse_error(err, src=None):
    def add_context(msg):
        if src and hasattr(err, "line"):
            lines = src.splitlines()
            if 1 <= err.line <= len(lines):
                code_line = lines[err.line - 1]
                underline  = " " * (err.column - 1) + "^"
                msg += f"\n    {code_line}\n    {underline}"
        return msg

    # Special cases for commas in lists/tables
    if hasattr(err, 'token') and hasattr(err, 'expected'):
        tok = err.token
        line_txt = src.splitlines()[err.line - 1] if src and err.line <= len(src.splitlines()) else ""
        stripped = line_txt.strip().replace(" ", "")
        if stripped in ("{,}", "[,]" ):
            msg = f"just a comma at line {err.line} (remove or add an item)."
            return add_context(msg)
        open_idx = max(line_txt.find("{"), line_txt.find("["))
        if open_idx != -1:
            after_open = line_txt[open_idx + 1 :].lstrip()
            if after_open.startswith(","):
                msg = "leading comma (remove the comma at the start)."
                return add_context(msg)
        before = line_txt[: err.column]
        if ",," in before.replace(" ", ""):
            msg = "double comma (remove one comma)."
            return add_context(msg)
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
            msg = "error: negative index not allowed"
        elif err.char == '"':
            msg = "error: index must be a number (text atoms cannot be used as indices)"
        else:
            msg = (
                f"Syntax error: Unexpected character '{err.char}' "
                f"at line {err.line}, column {err.column}."
            )
        return add_context(msg)
    elif hasattr(err, 'pos_in_stream'):
        msg = f"Syntax error: Unexpected input at position {err.pos_in_stream}."
        return add_context(msg)
    else:
        msg = f"Parse error: {err}"
        return add_context(msg)
