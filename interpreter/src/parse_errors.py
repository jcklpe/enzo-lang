# src/parse_errors.py

from lark import UnexpectedToken, UnexpectedInput, UnexpectedCharacters

def format_parse_error(err, src=None):
    """
    User-friendly error string for Lark parse errors, with code context
    and special cases for just-a-comma, leading comma, and double comma in lists/tables.
    """

    def add_context(msg):
        if src and hasattr(err, "line"):
            lines = src.splitlines()
            if 1 <= err.line <= len(lines):
                code_line = lines[err.line - 1]
                underline = " " * (err.column - 1) + "^"
                msg += f"\n    {code_line}\n    {underline}"
        return msg

    # --- Special cases for commas in lists/tables ---
    if isinstance(err, UnexpectedToken) and src:
        tok = err.token
        line_txt = src.splitlines()[err.line - 1] if err.line <= len(src.splitlines()) else ""
        stripped = line_txt.strip().replace(' ', '')

        # Just a comma as the only content
        if stripped in ('{,}', '[,]'):
            msg = f"just a comma at line {err.line} (remove or add an item)."
            return add_context(msg)

        # Leading comma: { ,foo:... } or [ ,1,... ]
        open_idx = max(line_txt.find('{'), line_txt.find('['))
        if open_idx != -1:
            after_open = line_txt[open_idx+1:].lstrip()
            if after_open.startswith(','):
                msg = f"leading comma at line {err.line} (remove the comma at the start)."
                return add_context(msg)

        # Double comma (e.g. 1,,2 or foo: 1,, bar: 2)
        before = line_txt[:err.column]
        if ',,' in before.replace(' ', ''):
            msg = f"double comma at line {err.line} (remove one comma)."
            return add_context(msg)

    # --- Default/fallback Lark parse errors (with context) ---
    if isinstance(err, UnexpectedToken):
        expected = ", ".join(err.expected)
        msg = (
            f"Syntax error: Unexpected token '{err.token}' at line {err.line}, column {err.column}.\n"
            f"Expected one of: {expected}"
        )
        return add_context(msg)
    elif isinstance(err, UnexpectedCharacters):
        msg = (
            f"Syntax error: Unexpected character '{err.char}' at line {err.line}, column {err.column}.\n"
            f"Allowed here: {err.allowed}"
        )
        return add_context(msg)
    elif isinstance(err, UnexpectedInput):
        msg = (
            f"Syntax error: Unexpected input at position {err.pos_in_stream}."
        )
        return add_context(msg)
    else:
        msg = f"Parse error: {err}"
        return add_context(msg)
