from src.parser       import parse
from src.ast_helpers  import Table, format_val
from collections import ChainMap
import sys

class InterpolationParseError(Exception):
    pass


_env = {}  # single global environment

# utility function
def force_value(val):
    global _env
    val = unwrap_single_block(val)
    while isinstance(val, tuple) and val[0] == "block_expr":
        _, params, bindings, stmts, is_multiline = unwrap_single_block(val)
        # If this is a multi-line block, check for explicit return statement
        if is_multiline:
            # If the last statement is not a ('return', ...), error
            if not stmts or (not isinstance(stmts[-1], tuple)) or stmts[-1][0] != "return":
                raise Exception("error: multi-line anonymous functions require explicit return")
        parent_env = _env
        local_env = {}
        _env = ChainMap(local_env, parent_env)
        try:
            for (name, expr) in params:
                local_env[name] = force_value(eval_ast(expr))
            for (name, expr) in bindings:
                local_env[name] = force_value(eval_ast(expr))
            result = None
            for stmt in stmts:
                result = force_value(eval_ast(stmt))
            val = result
        finally:
            _env = parent_env
    return val

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

def is_return_call(node):
    # Accept ("call", "return", [expr]) only
    return (
        isinstance(node, tuple)
        and node[0] == "call"
        and node[1] == "return"
        and isinstance(node[2], list)
        and len(node[2]) == 1
    )

def get_func_name(funcname):
    # Try as-is
    if funcname in _env:
        return funcname
    # Try adding/removing $
    if funcname.startswith('$'):
        alt = funcname[1:]
        if alt in _env:
            return alt
    else:
        alt = '$' + funcname
        if alt in _env:
            return alt
    raise NameError(f"undefined: {funcname}")

def unwrap_single_block(block):
    """
    If a block_expr only wraps a single block_expr, unwrap recursively.
    Prevents redundant nesting for parens and function bodies.
    """
    while (
        isinstance(block, tuple)
        and block[0] == "block_expr"
        and len(block[3]) == 1
        and isinstance(block[3][0], tuple)
        and block[3][0][0] == "block_expr"
    ):
        block = block[3][0]
    return block

# ── handle a block of multiple statements ─────────────────────────────
def eval_ast(node):
    global _env
    typ, *rest = node

    # if typ in ("block_expr", "bind", "bind_func", "expr"):
    #     print(f"eval_ast typ={typ} node={node}")

    # ── “block” means “evaluate each child in turn, return last” ───────
    if typ == "block":
        stmts = rest[0]                # a Python list of AST‐nodes
        result = None
        for stmt_node in stmts:
            # If stmt_node is a bare literal/var/list/table, eval as if it were an "expr"
            if (
                isinstance(stmt_node, tuple)
                and stmt_node
                and stmt_node[0] in ("var", "num", "str", "list", "table")
            ):
                result = eval_ast(("expr", stmt_node))
            else:
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
        return [force_value(eval_ast(el)) for el in children]

    if typ == "table":
        d = {}
        for (k, v_ast) in rest[0].items():
            d[k] = force_value(eval_ast(v_ast))
        return Table(d)

    if typ == "var":
        name = rest[0]
        if name not in _env:
            raise NameError(f"undefined: {name}")
        return force_value(_env[name])

    # --- function reference (object) ---
    if typ == "func_ref":
        funcname = rest[0]
        # Accept both with/without leading $
        if funcname in _env:
            val = _env[funcname]
        elif ('$' + funcname) in _env:
            val = _env['$' + funcname]
        else:
            raise NameError(f"undefined: {funcname}")
        if not isinstance(val, EnzoFunction):
            raise TypeError(f"{funcname} is not a function")
        return val

    # ── block_expr, block_body, block_item (local scope, param/default, explicit/implicit return) ──
    if typ == "block_expr":
        # Just return the tuple; don't execute here
        return (typ, *rest)

    if typ == "index_chain":
        # ("index_chain", base, [accessor1, accessor2...])
        base, *accessors = rest
        value = eval_ast(base)
        # If no accessors, just return base
        if not accessors:
            return value
        # Each accessor is a tuple: (kind, value)
        for accessor in accessors:
            if isinstance(accessor, tuple) and len(accessor) == 2:
                kind, val = accessor
                if kind == "DOTINT":
                    # 1-based index
                    idx = int(val)
                    if not isinstance(value, list):
                        raise TypeError("index applies to lists")
                    i = idx - 1
                    if i < 0 or i >= len(value):
                        raise IndexError("list index out of range")
                    value = value[i]
                elif kind == "DOTPROP":
                    if not isinstance(value, (dict, Table)):
                        raise TypeError("property access applies to tables")
                    if val not in value:
                        raise KeyError(val)
                    value = value[val]
                elif kind == "DOTVAR":
                    # variable property lookup
                    prop = val
                    if not isinstance(value, (dict, Table)):
                        raise TypeError("property access applies to tables")
                    if prop not in value:
                        raise KeyError(prop)
                    value = value[prop]
                else:
                    raise ValueError(f"unknown accessor kind {kind}")
            else:
                # Could be bare index: int or str
                value = value[accessor]
        return value

    # ── function call ──────────────────────────────────────────────────
    if typ == "call":
        funcname, args = rest
        if funcname == "return":
            if len(args) != 1:
                raise Exception("return() takes exactly one value")
            val = eval_ast(args[0])
            raise ReturnSignal(val)
        func = _env.get(get_func_name(funcname))
        # If this is a ("block_expr", ...), treat as lambda (call the block!)
        if isinstance(func, tuple) and func and func[0] == "block_expr":
            _, params, bindings, stmts, is_multiline = func
            parent_env = _env
            local_env = {}
            _env = ChainMap(local_env, parent_env)
            try:
                for (name, expr), arg in zip(params, args):
                    local_env[name] = eval_ast(arg)
                # fill missing params with defaults
                for i in range(len(args), len(params)):
                    local_env[params[i][0]] = eval_ast(params[i][1])
                for name, expr in bindings:
                    local_env[name] = eval_ast(expr)
                result = None
                for stmt in stmts:
                    result = eval_ast(stmt)
                return result
            finally:
                _env = parent_env
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
        return force_value(eval_ast(a)) + force_value(eval_ast(b))
    if typ == "sub":
        a, b = rest
        return force_value(eval_ast(a)) - force_value(eval_ast(b))
    if typ == "mul":
        a, b = rest
        return force_value(eval_ast(a)) * force_value(eval_ast(b))
    if typ == "div":
        a, b = rest
        return force_value(eval_ast(a)) / force_value(eval_ast(b))
    if typ == "neg":
        return -force_value(eval_ast(rest[0]))

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
    if typ in ("bind", "bind_func"):
        name, expr_ast = rest
        if name in _env:
            raise NameError(f"{name} already defined")
        # If this is a block_expr:
        if isinstance(expr_ast, tuple) and expr_ast[0] == "block_expr":
            # If this block_expr has any params or bindings, treat as a lambda and store it unevaluated.
            _, params, bindings, stmts, is_multiline = unwrap_single_block(expr_ast)
            if params or bindings or is_multiline:
                _env[name] = expr_ast
            else:
                # Single-expression, no params/bindings: eagerly evaluate, store result.
                _env[name] = force_value(expr_ast)
        else:
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
        inner = rest[0]
        val = eval_ast(inner)
        # If it's an anonymous block_expr (not assigned, not called), always eval immediately.
        if isinstance(val, tuple) and val[0] == "block_expr":
            _, params, bindings, stmts, is_multiline = unwrap_single_block(val)
            if not params and not bindings:
                # Multi-line anonymous requires explicit return at end
                if is_multiline and (not stmts or stmts[-1][0] != "return"):
                    raise Exception("error: multi-line anonymous functions require explicit return")
                # Always force evaluation for all top-level anonymous block_expr
                return force_value(val)
            else:
                # Named/parameterized blocks get returned as function/lambda
                return val
        else:
            return val

    # [DEBUG] Fallback for unknown node types: print AST node for diagnosis
    try:
        import pprint
        sys.stderr.write("unknown node encountered!\n")
        sys.stderr.write(f"node: {typ}\n")
        sys.stderr.write(pprint.pformat(node) + "\n")
        print(f"DEBUG unknown node: {node}", file=sys.stderr)
    except Exception:
        pass
    raise ValueError(f"unknown node: {typ}")

    # Fallback for unknown node types
    try:
        import pprint
        sys.stderr.write("unknown node encountered!\n")
        sys.stderr.write(f"node: {typ}\n")
        sys.stderr.write(pprint.pformat(node) + "\n")
    except Exception:
        pass
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
