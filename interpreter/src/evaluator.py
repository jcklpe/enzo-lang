from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, TableAtom, Binding, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode
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
        return f"<function ({', '.join(p[0] for p in self.params)}) ...>"

def eval_ast(node):
    global _env
    # AST node evaluation (object-based)
    if isinstance(node, NumberAtom):
        return node.value
    if isinstance(node, TextAtom):
        return _interp(node.value)
    if isinstance(node, ListAtom):
        return [eval_ast(el) for el in node.elements]
    if isinstance(node, TableAtom):
        return {k: eval_ast(v) for k, v in node.items}
    if isinstance(node, Binding):
        name = node.name
        if name in _env:
            raise EnzoRuntimeError(f"error: {error_message_already_defined(name)}")
        # Handle empty bind: $x: ;
        if node.value is None:
            _env[name] = Empty()
            return None  # Do not output anything for empty bind
        val = eval_ast(node.value)
        _env[name] = val
        return val
    if isinstance(node, VarInvoke):
        name = node.name
        if name not in _env:
            raise EnzoRuntimeError(error_message_unknown_variable(name))
        return _env[name]
    if isinstance(node, AddNode):
        return eval_ast(node.left) + eval_ast(node.right)
    if isinstance(node, SubNode):
        return eval_ast(node.left) - eval_ast(node.right)
    if isinstance(node, MulNode):
        return eval_ast(node.left) * eval_ast(node.right)
    if isinstance(node, DivNode):
        return eval_ast(node.left) / eval_ast(node.right)
    if isinstance(node, Invoke):
        func = eval_ast(node.func)
        args = [eval_ast(arg) for arg in node.args]
        if not isinstance(func, EnzoFunction):
            raise EnzoTypeError(error_message_not_a_function(func))
        call_env = func.closure_env.copy()
        for (param_name, default), arg in zip(func.params, args):
            call_env[param_name] = arg
        if len(args) < len(func.params):
            for (param_name, default) in func.params[len(args):]:
                call_env[param_name] = eval_ast(default)
        prev_env = _env
        _env = ChainMap(call_env, _env)
        try:
            res = None
            for stmt in func.body:
                res = eval_ast(stmt)
        except ReturnSignal as ret:
            _env = prev_env
            return ret.value
        finally:
            _env = prev_env
        return res
    if isinstance(node, FunctionAtom):
        # Return a function object (not invoked)
        return EnzoFunction(node.params, node.body, _env)
    if isinstance(node, Program):
        result = None
        for stmt in node.statements:
            result = eval_ast(stmt)
        return result
    # fallback for legacy tuple-based ASTs
    if isinstance(node, tuple):
        if node[0] == "rebind":
            name, value = node[1], node[2]
            if name not in _env:
                raise EnzoRuntimeError(f"error: cannot rebind undefined variable ${name}")
            old_val = _env[name]
            new_val = eval_ast(value)
            # Type locking: if old_val is Empty, allow any type; else, types must match
            if isinstance(old_val, Empty):
                _env[name] = new_val
                return new_val
            if type(new_val) != type(old_val):
                raise EnzoRuntimeError("error: cannot assign Text to Number" if isinstance(old_val, (int, float)) and isinstance(new_val, str)
                                       else f"error: cannot assign {type(new_val).__name__} to {type(old_val).__name__}")
            _env[name] = new_val
            return new_val
        raise EnzoRuntimeError(error_message_tuple_ast())
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
                val = eval_ast(expr_ast)
                val = _auto_invoke_if_fn(val)
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
