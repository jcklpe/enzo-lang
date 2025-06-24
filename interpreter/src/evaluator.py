from src.parser       import parse
from src.ast_helpers  import Table, format_val
from collections import ChainMap

class InterpolationParseError(Exception):
    pass


_env = {}  # single global environment

class FunctionAtomInstance:
    def __init__(self, params, body, closure_env):
        self.params = params          # list of (name, default)
        self.body = body              # list of AST stmts
        self.closure_env = closure_env.copy()  # captured env for closure

    def __repr__(self):
        return f"<function ({', '.join(p[0] for p in self.params)}) ...>"

def is_fn_atom(val):
    return isinstance(val, FunctionAtomInstance) or (isinstance(val, tuple) and val[0] == "function_atom")


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
            elif stmt[0] == "number":
                code_lines.append(f" {stmt[1]};")
            elif stmt[0] == "add":
                code_lines.append(f" {stmt[1]} + {stmt[2]};")
            else:
                code_lines.append(f" {stmt};")
        else:
            code_lines.append(f" {stmt};")
    block_str = "(\n" + "\n".join(code_lines) + "\n);"
    return block_str

def check_explicit_return(params, bindings, stmts, has_newline):
    """
    Require explicit return for all multi-line function atoms (named or anon).
    """
    if has_newline:
        has_return = any(isinstance(s, tuple) and s[0] == "return" for s in stmts)
        if not has_return:
            block_str = _pretty_block_error(params, bindings, stmts)
            raise ValueError(
                "multi-line function atoms require explicit return\n"
                + block_str +
                "\n    " + "^" * (len(block_str.strip()))
            )

def _auto_invoke_if_fn(val):
    global _env
    # function_atom auto-wrap to FunctionAtomInstance, check return rule if multi-line
    if isinstance(val, tuple) and val[0] == "function_atom":
        params, bindings, stmts, has_newline = val[1:]
        check_explicit_return(params, bindings, stmts, has_newline)
        fn = FunctionAtomInstance(params, stmts, _env)
        val = fn
    if isinstance(val, FunctionAtomInstance):
        call_env = val.closure_env.copy()
        # All parameters get their default values in auto-invoke context
        for (param_name, default) in val.params:
            call_env[param_name] = eval_ast(default) if default is not None else None
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
        stmts = rest[0]  # a Python list of AST‐nodes
        result = None
        for stmt_node in stmts:
            # TOP LEVEL: if it's a function_atom, auto-invoke it!
            if isinstance(stmt_node, tuple) and stmt_node[0] == "function_atom":
                result = _auto_invoke_if_fn(stmt_node)
            else:
                result = eval_ast(stmt_node)
        return result

    # ── literals / lookup ───────────────────────────────────────────────────────
    if typ == "number":
        return rest[0]

    if typ == "text":
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
    if typ == "function_atom":
        params, bindings, stmts, has_newline = rest
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

    # Note: function_atom is now always a function atom. Its invocation is handled by _auto_invoke_if_fn in all value contexts.


    # ── function call ──────────────────────────────────────────────────
    if typ == "call":
        # node = ("call", func_name, [args...])
        funcname, args = rest
        func = _env[funcname] if funcname in _env else _env.get('$' + funcname)
        if not isinstance(func, FunctionAtomInstance):
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
                call_env[param_name] = eval_ast(default) if default is not None else None
        _prev_env = _env
        _env = ChainMap(call_env, _prev_env)
        try:
            res = None
            for stmt in func.body:
                res = eval_ast(stmt)
        except ReturnSignal as ret:
            return ret.value
        finally:
            _env = _prev_env
        return res

    # ── return statement ───────────────────────────────────────────────
    if typ == "return":
        val = eval_ast(rest[0])
        raise ReturnSignal(val)

    # ── arithmetic ───────────────────────────────────────────────────────
    if typ == "add":
        a, b = rest
        aval = eval_ast(a)
        bval = eval_ast(b)
        return _auto_invoke_if_fn(aval) + _auto_invoke_if_fn(bval)
    if typ == "sub":
        a, b = rest
        aval = eval_ast(a)
        bval = eval_ast(b)
        return _auto_invoke_if_fn(aval) - _auto_invoke_if_fn(bval)
    if typ == "mul":
        a, b = rest
        aval = eval_ast(a)
        bval = eval_ast(b)
        return _auto_invoke_if_fn(aval) * _auto_invoke_if_fn(bval)
    if typ == "div":
        a, b = rest
        aval = eval_ast(a)
        bval = eval_ast(b)
        return _auto_invoke_if_fn(aval) / _auto_invoke_if_fn(bval)

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
        # Always store function_atom as FunctionAtomInstance, never auto-invoked!
        if isinstance(expr_ast, tuple) and expr_ast[0] == "function_atom":
            params, bindings, stmts, has_newline = expr_ast[1:]
            check_explicit_return(params, bindings, stmts, has_newline)
            fn = FunctionAtomInstance(params, stmts, _env)
            _env[name] = fn
            return fn
        # Otherwise, evaluate and store result as usual
        val = eval_ast(expr_ast)
        _env[name] = val
        return val

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
        out.append(s[i:j])
        k = s.find(">", j + 1)
        if k == -1:
            raise ValueError("unterminated interpolation in string")
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
