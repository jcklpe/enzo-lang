class Table(dict):
    def __repr__(self):
        # If empty, still show "{ }"
        if not self:
            return "{ }"
        pieces = []
        for key, val in self.items():
            # key already includes its leading "$"
            pieces.append(f"{key}: {format_val(val)}")
        return "{ " + ", ".join(pieces) + " }"

    __str__ = __repr__


def format_val(v):
    """
    Convert a Python value back into Enzo‐literal syntax:
      - Table → "{ $k1: val1, $k2: val2, … }"
      - list  → "[ val1, val2, … ]"
      - str   → "\"…\""
      - int   → "123"
      - other (float/bool/…) via str()
    """
    if isinstance(v, Table):
        return repr(v)
    if isinstance(v, dict):
        # If someone somehow passed a raw dict, cast to Table
        return repr(Table(v))

    if isinstance(v, list):
        if not v:
            return "[ ]"
        items = ", ".join(format_val(el) for el in v)
        return "[ " + items + " ]"

    if isinstance(v, str):
        return '"' + v.replace('"', r'\"') + '"'

    # For ints, floats, booleans, etc.
    return str(v)
