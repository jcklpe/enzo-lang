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
        return [eval_ast(el) for el in rest[0]]

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
        if name in _env:
            raise NameError(f"{name} already defined")
        _env[name] = eval_ast(expr_ast)
        return _env[name]

    if typ == "rebind":
        name, expr_ast = rest
        _env[name] = eval_ast(expr_ast)
        return _env[name]

    # ── bare expression statement ─────────────────────────────────────────
    if typ == "expr":
        return eval_ast(rest[0])

    raise ValueError(f"unknown node: {typ}")


# ── string‐interpolation helper ───────────────────────────────────────────
def _interp(s: str):
    """
    Given a Python string `s`, expand each “<expr>” by:
      1) parse “expr”
      2) evaluate it
      3) convert result to str
    """
    if "<" not in s:
        return s

    out, i = [], 0
    while i < len(s):
        j = s.find("<", i)
        if j == -1:
            out.append(s[i:])
            break
        out.append(s[i:j])
        k = s.find(">", j + 1)
        if k == -1:
            raise ValueError("unterminated interpolation in string")
        expr_src = s[j + 1 : k].strip()
        expr_ast = parse(expr_src)
        out.append(str(eval_ast(expr_ast)))
        i = k + 1

    return "".join(out)
