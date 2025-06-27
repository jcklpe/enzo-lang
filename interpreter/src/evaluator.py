from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, TableAtom, Binding, BindOrRebind, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode
from src.error_handling import InterpolationParseError, ReturnSignal, EnzoRuntimeError, EnzoTypeError
from src.error_messaging import (
    error_message_already_defined,
    error_message_unknown_variable,
    error_message_not_a_function,
    error_message_tuple_ast,
    error_message_unknown_node,
    error_message_unterminated_interpolation,
)

_env = {}  # single global environment

class EnzoFunction:
    def __init__(self, params, body, closure_env):
        self.params = params          # list of (name, default)
        self.body = body              # list of AST stmts
        self.closure_env = closure_env.copy()  # captured env for closure

    def __repr__(self):
        return f"<function ({', '.join(self.params)}) ...>"

def _auto_invoke_if_fn(val, node=None, value_demand=False, already_invoked=False):
    # Only auto-invoke if val is an EnzoFunction and node is a FunctionAtom or VarInvoke (i.e., an AST node)
    if value_demand and isinstance(val, EnzoFunction) and not already_invoked:
        if isinstance(node, (FunctionAtom, VarInvoke)):
            # Pass already_invoked=True to prevent infinite recursion
            return eval_ast(Invoke(node, []), value_demand=True, already_invoked=True)
        # If node is not an AST node, just return the value
        return val
    return val

def eval_ast(node, value_demand=False, already_invoked=False):
    global _env
    # If this is a top-level FunctionAtom, always treat as value-demand
    if isinstance(node, FunctionAtom) and not value_demand:
        return eval_ast(Invoke(node, []), value_demand=True, already_invoked=True)

    # AST node evaluation (object-based)
    if isinstance(node, NumberAtom):
        return node.value
    if isinstance(node, TextAtom):
        return _interp(node.value)
    if isinstance(node, ListAtom):
        # print(f"[DEBUG] ListAtom: {node.elements}")
        return [_auto_invoke_if_fn(eval_ast(el, value_demand=True), el, value_demand=True, already_invoked=already_invoked) for el in node.elements]
    if isinstance(node, TableAtom):
        return {k: _auto_invoke_if_fn(eval_ast(v, value_demand=True), v, value_demand=True, already_invoked=already_invoked) for k, v in node.items}
    if isinstance(node, Binding):
        name = node.name
        if name in _env:
            raise EnzoRuntimeError(f"error: {error_message_already_defined(name)}")
        # Handle empty bind: $x: ;
        if node.value is None:
            _env[name] = Empty()
            return None  # Do not output anything for empty bind
        # If value is a FunctionAtom, store as function object, not result
        if isinstance(node.value, FunctionAtom):
            _env[name] = EnzoFunction(node.value.params, node.value.body, _env)
            return _env[name]
        val = eval_ast(node.value, value_demand=False)  # storage context
        _env[name] = val
        return val
    if isinstance(node, VarInvoke):
        name = node.name
        if name not in _env:
            raise EnzoRuntimeError(error_message_unknown_variable(name))
        val = _env[name]
        # print(f"[DEBUG] VarInvoke: {name} -> {val!r}")
        return _auto_invoke_if_fn(val, node, value_demand, already_invoked=already_invoked)
    if isinstance(node, AddNode):
        left = eval_ast(node.left, value_demand=True)
        right = eval_ast(node.right, value_demand=True)
        return left + right
    if isinstance(node, SubNode):
        left = eval_ast(node.left, value_demand=True)
        right = eval_ast(node.right, value_demand=True)
        return left - right
    if isinstance(node, MulNode):
        left = eval_ast(node.left, value_demand=True)
        right = eval_ast(node.right, value_demand=True)
        return left * right
    if isinstance(node, DivNode):
        left = eval_ast(node.left, value_demand=True)
        right = eval_ast(node.right, value_demand=True)
        return left / right
    if isinstance(node, Invoke):
        func = eval_ast(node.func, value_demand=True, already_invoked=True)
        args = [eval_ast(arg, value_demand=True, already_invoked=already_invoked) for arg in node.args]
        if not isinstance(func, EnzoFunction):
            raise EnzoTypeError(error_message_not_a_function(func))
        call_env = func.closure_env.copy()
        for (param_name, default), arg in zip(func.params, args):
            call_env[param_name] = arg
        if len(args) < len(func.params):
            for (param_name, default) in func.params[len(args):]:
                call_env[param_name] = eval_ast(default, value_demand=True)
        prev_env = _env
        _env = ChainMap(call_env, _env)
        try:
            res = None
            for stmt in func.body:
                res = eval_ast(stmt, value_demand=True)
        except ReturnSignal as ret:
            _env = prev_env
            return ret.value
        finally:
            _env = prev_env
        return res
    if isinstance(node, FunctionAtom):
        fn = EnzoFunction(node.params, node.body, _env)
        return _auto_invoke_if_fn(fn, node, value_demand, already_invoked=already_invoked)
    if isinstance(node, Program):
        result = None
        stmts = node.statements
        n = len(stmts)
        for i, stmt in enumerate(stmts):
            if i == n - 1:
                result = eval_ast(stmt, value_demand=True, already_invoked=already_invoked)
            else:
                eval_ast(stmt, value_demand=False, already_invoked=already_invoked)
        return _auto_invoke_if_fn(result, node, True, already_invoked=already_invoked)
    if isinstance(node, list):
        result = None
        n = len(node)
        for i, stmt in enumerate(node):
            if i == n - 1:
                result = eval_ast(stmt, value_demand=True, already_invoked=already_invoked)
            else:
                eval_ast(stmt, value_demand=False, already_invoked=already_invoked)
        return _auto_invoke_if_fn(result, node, True, already_invoked=already_invoked)
    # fallback for legacy tuple-based ASTs
    if isinstance(node, tuple):
        if node[0] == "rebind":
            name, value = node[1], node[2]
            new_val = eval_ast(value, value_demand=True)
            if name not in _env:
                _env[name] = new_val
                return new_val
            old_val = _env[name]
            if isinstance(old_val, Empty):
                _env[name] = new_val
                return new_val
            if type(new_val) != type(old_val):
                raise EnzoRuntimeError("error: cannot assign Text to Number" if isinstance(old_val, (int, float)) and isinstance(new_val, str)
                                       else f"error: cannot assign {type(new_val).__name__} to {type(old_val).__name__}")
            _env[name] = new_val
            return new_val
        raise EnzoRuntimeError(error_message_tuple_ast())
    if isinstance(node, BindOrRebind):
        name = node.target
        val = eval_ast(node.value, value_demand=False)  # storage context
        if name not in _env:
            _env[name] = val
            return val
        old_val = _env[name]
        if isinstance(old_val, Empty):
            _env[name] = val
            return val
        if type(val) != type(old_val):
            raise EnzoRuntimeError("error: cannot assign Text to Number" if isinstance(old_val, (int, float)) and isinstance(val, str)
                                   else f"error: cannot assign {type(val).__name__} to {type(old_val).__name__}")
        _env[name] = val
        return val
    raise EnzoRuntimeError(error_message_unknown_node(node))

# ── text_atom‐interpolation helper ───────────────────────────────────────────
def _interp(s: str):
    # Given a Python string `s`, expand each “<expr>” by:
    #   - Allow multiple expressions separated by semicolons inside "<...>"
    #   - Evaluate each sub‐expression (parse+eval)
    #   - Convert each result to str and concatenate in order.
    # Examples:
    #   "<$a; $b;>" → str(eval($a)) + str(eval($b))
    #   "<1 + 2; 3 * 4;>" → "3" + "12" = "312"

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
            raise EnzoRuntimeError(error_message_unterminated_interpolation())
        expr_src = s[j + 1 : k].strip()
        parts = [p.strip() for p in expr_src.split(";") if p.strip()]
        concatenated = ""
        for part in parts:
            try:
                expr_ast = parse(part)
                val = eval_ast(expr_ast, value_demand=True)
                concatenated += str(val)
            except Exception:
                raise InterpolationParseError()
        out.append(concatenated)
        i = k + 1
    return "".join(out)

# Sentinel for uninitialized/empty binds
class Empty:
    def __repr__(self):
        return "<empty>"
