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
    return f"Unexpected token: {token}"

def error_message_cannot_assign(new_type, old_type):
    return f"error: cannot assign {new_type} to {old_type}"

def error_message_double_minus(token=None):
    return "error: double minus not allowed"

def error_message_list_index_out_of_range():
    return "error: list index out of range"

def error_message_cant_use_text_as_index():
    return "error: can't use text as index"

def error_message_index_applies_to_lists():
    return "error: index applies to lists"

def error_message_table_property_not_found(prop):
    return f"error: table property not found: ${prop}"

def error_message_index_must_be_number():
    return "error: index must be a number (text atoms cannot be used as indices)"

def error_message_index_must_be_integer():
    return "error: index must be an integer"

def error_message_assignment_to_list_index_out_of_range():
    return "error: list index out of range"

def error_message_unmatched_bracket():
    return "error: unmatched bracket"

def error_message_unmatched_parenthesis():
    return "error: unmatched parenthesis"

def error_message_unmatched_brace():
    return "error: unmatched brace"

def error_message_double_comma():
    return "error: double comma in list"

def error_message_empty_list_comma():
    return "error: empty list with just a comma"

def error_message_excess_leading_comma():
    return "error: excess leading comma"

def error_message_cannot_assign_target(target):
    return f"Cannot assign to target: {target}"

def error_message_unexpected_character(char, pos):
    return f"Unexpected character: {char!r} at {pos}"

def error_message_parse_error_in_interpolation():
    return "error: parse error in interpolation"

def error_message_pipeline_expects_function():
    return "error: pipeline expects function atom after `then`"

# User-friendly error message for parse errors, with code context.
def format_parse_error(err, src=None):
    from src.error_messaging import error_message_with_code_line
    # If the error has a code_line attribute, use it for context
    if hasattr(err, 'code_line') and err.code_line:
        return error_message_with_code_line(str(err), err.code_line)
    # Special cases for commas in lists/tables and parse errors
    if hasattr(err, 'token') and hasattr(err, 'expected'):
        # ...existing parse error logic...
        # (leave as is)
        pass
    # For all other errors, if src is provided, always add the code line
    if src:
        # Strip comments from source code for error context
        code_line = src.strip()
        if '//' in code_line:
            code_line = code_line.split('//', 1)[0].rstrip()
        return error_message_with_code_line(str(err), code_line)
    return str(err)

def error_message_with_code_line(msg, code_line):
    #Format an error message with the code line, no caret, for golden file compatibility.
    return f"{msg}\n    {code_line}"

def error_message_double_comma_table():
    return "error: extra comma in table"

def error_message_leading_comma_table():
    return "error: leading comma in table"

def error_message_empty_table_comma():
    return "error: empty table with comma"

def error_message_cannot_declare_this():
    return "error: cannot declare variable '$this'"

def error_message_multiline_function_requires_return():
    return "error: multi-line anonymous functions require explicit return"

def error_message_param_outside_function():
    return "error: param declarations can only be used inside function definitions"

def error_message_too_many_args():
    return "error: too many args"

def error_message_arg_type_mismatch(param_name, expected_type, actual_type):
    return f"error: expected argument is a {expected_type} atom, not a {actual_type} atom"
