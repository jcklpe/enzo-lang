from src.parser       import parse
from src.ast_helpers  import Table, format_val

class InterpolationParseError(Exception):
    pass


_env = {}  # single global environment

class EnzoFunction:
    def __init__(self, params, body, closure_env):
        self.params = params          # list of (name, default)
        self.body = body              # list of AST stmts
        self.closure_env = closure_env.copy()  # captured env for closure

    def __repr__(self):
        return f"<function ({', '.join(p[0] for p in self.params)}) ...>"

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

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

    # ── literals / lookup ───────────────────────────────────────────────────────
    if typ == "num":
        return rest[0]

    if typ == "str":
        return _interp(rest[0])

    if typ == "list":
        children = rest[0] if rest else []
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

    # ── function literal ────────────────────────────────────────────────
    if typ == "function":
        # node = ("function", ("function_body", params, body))
        _tag, params, body = rest[0]
        param_pairs = []
        for p in params:
            # ("param", name, default)
            param_pairs.append((p[1], p[2]))
        # Disallow 0-param single-line anon fns
        if len(param_pairs) == 0 and isinstance(body, list) and len(body) == 1 and not isinstance(body[0], tuple):
            raise TypeError("Anonymous functions must declare at least one parameter.")
        return EnzoFunction(param_pairs, body, _env.copy())

    # ── function call ──────────────────────────────────────────────────
    if typ == "call":
        # node = ("call", func_name, [args...])
        funcname, args = rest
        func = _env[funcname]
        if not isinstance(func, EnzoFunction):
            raise TypeError(f"{funcname} is not a function")
        if len(args) > len(func.params):
            raise TypeError("Too many arguments for function call")
        call_env = func.closure_env.copy()
        # Evaluate provided arguments
        for (param_name, default), arg in zip(func.params, args):
            call_env[param_name] = eval_ast(arg)
        # Fill in any missing params using their defaults
        if len(args) < len(func.params):
            for (param_name, default) in func.params[len(args):]:
                call_env[param_name] = eval_ast(default)
        # Run body in this new env
        try:
            res = None
            for stmt in func.body:
                res = eval_ast(stmt)
        except ReturnSignal as ret:
            return ret.value
        return res

    # ── return statement ───────────────────────────────────────────────
    if typ == "return":
        val = eval_ast(rest[0])
        raise ReturnSignal(val)

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

    # ── single‐property or list‐index rebind (“expr .prop <: expr” or “expr .idx <: expr”) ─
    if typ == "prop_rebind":
        base_node, new_expr = rest

        # Support rebinding for both ("attr", ...) (table property) and ("index", ...) (list element)
        if isinstance(base_node, tuple):
            # Table property: ("attr", table_node, prop_name)
            if base_node[0] == "attr":
                _, table_node, prop_name = base_node
                tbl = eval_ast(table_node)
                if not isinstance(tbl, (dict, Table)):
                    raise TypeError("property rebind applies to tables")
                if prop_name not in tbl:
                    raise KeyError(f"'{prop_name}' not found for rebinding")
                new_val = eval_ast(new_expr)
                tbl[prop_name] = new_val
                return new_val

            # List element: ("index", list_node, idx_node)
            elif base_node[0] == "index":
                _, list_node, idx_node = base_node
                seq = eval_ast(list_node)
                idx = eval_ast(idx_node)
                if not isinstance(seq, list):
                    raise TypeError("index applies to lists")
                if not isinstance(idx, int):
                    raise TypeError("index must be a number")
                i = idx - 1
                if i < 0 or i >= len(seq):
                    raise IndexError("list index out of range")
                new_val = eval_ast(new_expr)
                seq[i] = new_val
                return new_val

        raise TypeError("property rebind applies to tables or lists")

    # ── bind / rebind ─────────────────────────────────────────────────────
    if typ == "bind":
        name, expr_ast = rest
        # Disallow redeclaration, even if it's still None (empty)
        if name in _env:
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
            try:
                # For each sub‐expression, parse and evaluate it
                expr_ast = parse(part)
                val = eval_ast(expr_ast)
                concatenated += str(val)
            except Exception:
                # Raise a special error so the outer code can format it
                raise InterpolationParseError()
        out.append(concatenated)

        i = k + 1

    return "".join(out)
