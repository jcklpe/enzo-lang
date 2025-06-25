from src.parser       import parse
from src.ast_helpers  import Table, format_val
from collections import ChainMap

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

# ── helper for auto-invoking function objects in any value context ──
def _pretty_block_error(params, bindings, stmts):
    code_lines = []
    for stmt in stmts:
        if isinstance(stmt, tuple):
            if stmt[0] == "bind":
                code_lines.append(f" ${stmt[1]}: {stmt[2]};")
            elif stmt[0] == "number_atom":
                code_lines.append(f" {stmt[1]};")
            elif stmt[0] == "add":
                code_lines.append(f" {stmt[1]} + {stmt[2]};")
            else:
                code_lines.append(f" {stmt};")
        else:
            code_lines.append(f" {stmt};")
    block_str = "(\n" + "\n".join(code_lines) + "\n);"
    return block_str

def check_explicit_return(params, bindings, stmts):
    # Enforce: If block has >1 statement and no return, it's an error.
    has_return = any(isinstance(s, tuple) and s[0] == "return" for s in stmts)
    if len(stmts) > 1 and not has_return:
        block_str = _pretty_block_error(params, bindings, stmts)
        raise ValueError(
            "multi-line anonymous functions require explicit return\n"
            + block_str +
            "\n    " + "^" * (len(block_str.strip()))
        )

def _auto_invoke_if_fn(val):
    global _env
    if isinstance(val, tuple) and val[0] == "block_expr":
        params, bindings, stmts, has_newline = val[1:]
        # Only enforce error for direct evaluation
        check_explicit_return(params, bindings, stmts)
        if len(stmts) == 1:
            return eval_ast(stmts[0])
        val = EnzoFunction(params, stmts, _env)
    if isinstance(val, EnzoFunction):
        # Bind parameters with defaults in a new local environment
        call_env = val.closure_env.copy()
        for param_name, default in val.params:
            call_env[param_name] = eval_ast(default)
        _prev_env = _env
        _env = ChainMap(call_env, _prev_env)
        try:
            res = None
            for stmt in val.body:
                res = eval_ast(stmt)
            return res
        except ReturnSignal as ret:
            return ret.value
        finally:
            _env = _prev_env
    return val

# ── handle a block of multiple statements ─────────────────────────────
def eval_ast(node):
    global _env
    typ, *rest = node

    # ── “block” means “evaluate each child in turn, return last” ───────
    if typ == "block":
        stmts = rest[0]                # a Python list of AST‐nodes
        result = None
        for stmt_node in stmts:
            result = eval_ast(stmt_node)
        return result

    # ── literals / lookup ───────────────────────────────────────────────────────
    if typ == "number_atom":
        return rest[0]

    if typ == "text_atom":
        return _interp(rest[0])

    if typ == "list":
        children = rest[0] if rest else []
        if children == [None]:
            children = []
        # DO NOT auto-invoke! Just store as returned.
        return [eval_ast(el) for el in children]

    if typ == "table":
        d = {}
        for (k, v_ast) in rest[0].items():
            d[k] = eval_ast(v_ast)
        return Table(d)

    if typ == "var":
        name = rest[0]
        # Try raw name, then without $ if not found
        if name not in _env:
            alt_name = name[1:] if name.startswith('$') else ('$' + name)
            if alt_name in _env:
                name = alt_name
            else:
                raise NameError(f"undefined: {name}")
        val = _env[name]
        return _auto_invoke_if_fn(val)

    # ── block expression as value/expression ──
    if typ == "block_expr":
        params, bindings, stmts, has_newline = rest
        check_explicit_return(params, bindings, stmts)
        local_env = {}
        for name, default in params:
            local_env[name] = eval_ast(default) if default is not None else None
        for name, expr in bindings:
            local_env[name] = eval_ast(expr)
        prev_env = _env
        _env = ChainMap(local_env, _env)
        try:
            res = None
            for stmt in stmts:
                res = eval_ast(stmt)
        except ReturnSignal as ret:
            _env = prev_env
            return ret.value
        finally:
            _env = prev_env
        return res

    # Note: block_expr is now always a function atom. Its invocation is handled by _auto_invoke_if_fn in all value contexts.


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
        return _auto_invoke_if_fn(eval_ast(a)) + _auto_invoke_if_fn(eval_ast(b))
    if typ == "sub":
        a, b = rest
        return _auto_invoke_if_fn(eval_ast(a)) - _auto_invoke_if_fn(eval_ast(b))
    if typ == "mul":
        a, b = rest
        return _auto_invoke_if_fn(eval_ast(a)) * _auto_invoke_if_fn(eval_ast(b))
    if typ == "div":
        a, b = rest
        return _auto_invoke_if_fn(eval_ast(a)) / _auto_invoke_if_fn(eval_ast(b))

    # ── list indexing (1-based) ────────────────────────────────────────
    if typ == "index":
        base_ast, idx_ast = rest
        seq = eval_ast(base_ast)
        # Accept both ('number_atom', n) and int for indices
        if isinstance(idx_ast, tuple) and idx_ast[0] == "number_atom":
            idx = idx_ast[1]
        else:
            idx = eval_ast(idx_ast) if isinstance(idx_ast, tuple) else idx_ast
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
        key_dollar = f"${prop_name}" if not prop_name.startswith("$") else prop_name
        key_plain = prop_name.lstrip("$")
        if key_dollar in tbl:
            return tbl[key_dollar]
        if key_plain in tbl:
            return tbl[key_plain]
        raise Exception(f"'{key_dollar}'")

    # ── single‐property or list‐index rebind (“expr .prop <: expr” or “expr .idx <: expr”) ─
    if typ == "prop_rebind":
        base_node, new_expr = rest

        if isinstance(base_node, tuple):
            # Table property: ("attr", table_node, prop_name)
            if base_node[0] == "attr":
                _, table_node, prop_name = base_node
                tbl = eval_ast(table_node)
                if not isinstance(tbl, (dict, Table)):
                    raise TypeError("property rebind applies to tables")
                key_dollar = f"${prop_name}" if not prop_name.startswith("$") else prop_name
                key_plain = prop_name.lstrip("$")
                if key_dollar in tbl:
                    tbl[key_dollar] = eval_ast(new_expr)
                    return tbl[key_dollar]
                if key_plain in tbl:
                    tbl[key_plain] = eval_ast(new_expr)
                    return tbl[key_plain]
                # Always error as error: '$prop' not found for rebinding (no extra quotes)
                raise Exception(f"'{key_dollar}' not found for rebinding")

            # List element: ("index", list_node, idx_node)
            elif base_node[0] == "index":
                _, list_node, idx_node = base_node
                seq = eval_ast(list_node)
                # Accept both ('number_atom', n) and int for indices
                if isinstance(idx_node, tuple) and idx_node[0] == "number_atom":
                    idx = idx_node[1]
                else:
                    idx = eval_ast(idx_node) if isinstance(idx_node, tuple) else idx_node
                if not isinstance(seq, list):
                    raise TypeError("index applies to lists")
                if not isinstance(idx, int):
                    raise TypeError("index must be a number")
                i = idx - 1
                if i < 0 or i >= len(seq):
                    raise IndexError("list index out of range")
                seq[i] = eval_ast(new_expr)
                return seq[i]

        raise TypeError("property rebind applies to tables or lists")

    # ── bind / rebind ─────────────────────────────────────────────────────
    if typ == "bind":
        name, expr_ast = rest
        # Disallow redeclaration, even if it's still None (empty)
        if name in _env:
            raise NameError(f"{name} already defined")
        # If the right-hand side is a block_expr, store as a function, not its value!
        if isinstance(expr_ast, tuple) and expr_ast[0] == "block_expr":
            params, bindings, stmts, is_multiline = expr_ast[1:]
            fn = EnzoFunction(params, stmts, _env)
            _env[name] = fn
            return fn
        # Otherwise, evaluate and store result as usual
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
        return _auto_invoke_if_fn(eval_ast(rest[0]))


    raise ValueError(f"unknown node: {typ}")


# ── text_atom‐interpolation helper ───────────────────────────────────────────
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
        out.append(s[i:j])
        k = s.find(">", j + 1)
        if k == -1:
            raise ValueError("unterminated interpolation in text_atom")
        expr_src = s[j + 1 : k].strip()
        parts = [p.strip() for p in expr_src.split(";") if p.strip()]
        concatenated = ""
        for part in parts:
            try:
                expr_ast = parse(part)
                val = eval_ast(expr_ast)
                val = _auto_invoke_if_fn(val)
                concatenated += str(val)
            except Exception:
                raise InterpolationParseError()
        out.append(concatenated)
        i = k + 1
    return "".join(out)
