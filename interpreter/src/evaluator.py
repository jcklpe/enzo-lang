from src.parser       import parse
from src.ast_helpers  import Table, format_val

_env = {}  # single global environment

# ── handle a block of multiple statements ─────────────────────────────
def eval_ast(node):
    typ, *rest = node

    # ── “block” means “evaluate each child in turn, return last” ───────
    if typ == "block":
        stmts = rest[0]                # a Python list of AST‐nodes
        result = None
        for stmt_node in stmts:
            result = eval_ast(stmt_node)
        return result

    # ── literals / lookup ───────────────────────────────────────────────
    if typ == "num":
        return rest[0]

    if typ == "str":
        return _interp(rest[0])

    if typ == "list":
    # Defensive: always turn rest[0] into a real list of AST nodes
        children = rest[0] if rest else []
        # If children is [None], treat as []
        if children == [None]:
            children = []
        return [eval_ast(el) for el in children]

    if typ == "table":
        d = {}
        for (k, v_ast) in rest[0].items():
            d[k] = eval_ast(v_ast)
        return Table(d)

    if typ == "var":
        name = rest[0]
        if name not in _env:
            raise NameError(f"undefined: {name}")
        return _env[name]

    # ── arithmetic ───────────────────────────────────────────────────────
    if typ == "add":
        a, b = rest
        return eval_ast(a) + eval_ast(b)
    if typ == "sub":
        a, b = rest
        return eval_ast(a) - eval_ast(b)
    if typ == "mul":
        a, b = rest
        return eval_ast(a) * eval_ast(b)
    if typ == "div":
        a, b = rest
        return eval_ast(a) / eval_ast(b)

    # ── list indexing (1-based) ────────────────────────────────────────
    if typ == "index":
        base_ast, idx_ast = rest
        seq = eval_ast(base_ast)
        idx = eval_ast(idx_ast)
        if not isinstance(seq, list):
            raise TypeError("index applies to lists")
        if not isinstance(idx, int):
            raise TypeError("index must be a number")
        i = idx - 1
        if i < 0 or i >= len(seq):
            raise IndexError("list index out of range")
        return seq[i]

    # ── table property access ───────────────────────────────────────────
    if typ == "attr":
        base_ast, prop_name = rest
        tbl = eval_ast(base_ast)
        if not isinstance(tbl, (dict, Table)):
            raise TypeError("property access applies to tables")
        if prop_name not in tbl:
            raise KeyError(prop_name)
        return tbl[prop_name]

    # ── single‐property rebind (“expr .prop <: expr”) ─────────────────────
    if typ == "prop_rebind":
        # rest is [ baseAST(for “$tbl.name”), exprAST ]
        base_node, new_expr = rest
        # base_node must be ("attr", tableNode, "$prop")
        _, table_node, prop_name = base_node
        tbl = eval_ast(table_node)
        if not isinstance(tbl, (dict, Table)):
            raise TypeError("property rebind applies to tables")
        new_val = eval_ast(new_expr)
        tbl[prop_name] = new_val
        return new_val

    # ── bind / rebind ─────────────────────────────────────────────────────
    if typ == "bind":
        name, expr_ast = rest
        # If the name already exists and is still "empty" (i.e. None), fill it.
        if name in _env:
            if _env[name] is None:
                new_val = eval_ast(expr_ast)
                _env[name] = new_val
                return new_val
            # If it existed and was not None, disallow re-declaration with `:`
            raise NameError(f"{name} already defined")

        # Fresh bind (name not present at all)
        _env[name] = eval_ast(expr_ast)
        return _env[name]

    if typ == "bind_empty":
        name = rest[0]
        if name in _env:
            raise NameError(f"{name} already defined")
        # Represent “empty/untyped” by storing Python None
        _env[name] = None
        return None

    if typ == "rebind":
        name, expr_ast = rest
        new_val = eval_ast(expr_ast)

        # If never declared, treat `<:` or `:>` as a fresh bind
        if name not in _env:
            _env[name] = new_val
            return new_val

        old_val = _env[name]

        # If old_val is None, this is the first non‐empty assignment → lock in new type
        if old_val is None:
            _env[name] = new_val
            return new_val

        # Otherwise, enforce that types match
        if type(old_val) is not type(new_val):
            # Helper to give friendly type names
            def pretty_type(x):
                if isinstance(x, str):
                    return "Text"
                if isinstance(x, int):
                    return "Number"
                if isinstance(x, list):
                    return "List"
                if isinstance(x, (dict, Table)):
                    return "Table"
                # fallback
                return type(x).__name__

            msg = f"cannot assign {pretty_type(new_val)} to {pretty_type(old_val)}"
            raise TypeError(msg)

        # Types match → perform rebind
        _env[name] = new_val
        return new_val

    # ── bare expression statement ─────────────────────────────────────────
    if typ == "expr":
        return eval_ast(rest[0])

    raise ValueError(f"unknown node: {typ}")


# ── string‐interpolation helper ───────────────────────────────────────────
def _interp(s: str):
    """
    Given a Python string `s`, expand each “<expr>” by:
      - Allow multiple expressions separated by semicolons inside "<...>"
      - Evaluate each sub‐expression (parse+eval)
      - Convert each result to str and concatenate in order.

    Examples:
      "<$a; $b;>" → str(eval($a)) + str(eval($b))
      "<1 + 2; 3 * 4;>" → "3" + "12" = "312"
    """
    if "<" not in s:
        return s

    out, i = [], 0
    while i < len(s):
        j = s.find("<", i)
        if j == -1:
            out.append(s[i:])
            break
        # Append text before "<"
        out.append(s[i:j])

        # Find closing ">"
        k = s.find(">", j + 1)
        if k == -1:
            raise ValueError("unterminated interpolation in string")

        # Extract inside-of-<...>, including any semicolons
        expr_src = s[j + 1 : k].strip()
        # Split on semicolons to allow multiple expressions
        parts = [p.strip() for p in expr_src.split(";") if p.strip()]
        concatenated = ""
        for part in parts:
            # For each sub‐expression, parse and evaluate it
            expr_ast = parse(part)
            val = eval_ast(expr_ast)
            concatenated += str(val)
        out.append(concatenated)

        i = k + 1

    return "".join(out)
