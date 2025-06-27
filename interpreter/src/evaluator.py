from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, TableAtom, Binding, BindOrRebind, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode, FunctionRef
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

def invoke_function(fn, args, env):
    if not isinstance(fn, EnzoFunction):
        raise EnzoTypeError(error_message_not_a_function(fn))
    call_env = fn.closure_env.copy()
    for (param_name, default), arg in zip(fn.params, args):
        call_env[param_name] = arg
    if len(args) < len(fn.params):
        for (param_name, default) in fn.params[len(args):]:
            call_env[param_name] = eval_ast(default, value_demand=True, env=ChainMap(call_env, env))
    local_env = ChainMap(call_env, env)
    try:
        res = None
        for stmt in fn.body:
            res = eval_ast(stmt, value_demand=True, env=local_env)
    except ReturnSignal as ret:
        return ret.value
    return res


def eval_ast(node, value_demand=False, already_invoked=False, env=None):
    if env is None:
        env = _env
    if isinstance(node, NumberAtom):
        return node.value
    if isinstance(node, TextAtom):
        return _interp(node.value)
    if isinstance(node, ListAtom):
        return [eval_ast(el, value_demand=True, env=env) for el in node.elements]
    if isinstance(node, TableAtom):
        return {k: eval_ast(v, value_demand=True, env=env) for k, v in node.items}
    if isinstance(node, Binding):
        name = node.name
        if name in env:
            raise EnzoRuntimeError(f"error: {error_message_already_defined(name)}")
        # Handle empty bind: $x: ;
        if node.value is None:
            env[name] = Empty()
            return None  # Do not output anything for empty bind
        # If value is a FunctionAtom, store as function object, not result
        if isinstance(node.value, FunctionAtom):
            env[name] = EnzoFunction(node.value.params, node.value.body, env)
            return env[name]
        val = eval_ast(node.value, value_demand=False, env=env)  # storage context
        env[name] = val
        return val
    if isinstance(node, VarInvoke):
        name = node.name
        if name not in env:
            raise EnzoRuntimeError(error_message_unknown_variable(name))
        val = env[name]
        # Demand-value context: invoke if function
        if value_demand and isinstance(val, EnzoFunction):
            return invoke_function(val, [], env)
        return val
    if isinstance(node, FunctionRef):
        name = node.name
        if name not in env:
            raise EnzoRuntimeError(error_message_unknown_variable(name))
        val = env[name]
        if not isinstance(val, EnzoFunction):
            raise EnzoTypeError(error_message_not_a_function(val))
        return val
    if isinstance(node, FunctionAtom):
        # Demand-value context: invoke
        if value_demand:
            fn = EnzoFunction(node.params, node.body, env)
            return invoke_function(fn, [], env)
        else:
            return EnzoFunction(node.params, node.body, env)
    if isinstance(node, AddNode):
        left = eval_ast(node.left, value_demand=True, env=env)
        right = eval_ast(node.right, value_demand=True, env=env)
        return left + right
    if isinstance(node, SubNode):
        left = eval_ast(node.left, value_demand=True, env=env)
        right = eval_ast(node.right, value_demand=True, env=env)
        return left - right
    if isinstance(node, MulNode):
        left = eval_ast(node.left, value_demand=True, env=env)
        right = eval_ast(node.right, value_demand=True, env=env)
        return left * right
    if isinstance(node, DivNode):
        left = eval_ast(node.left, value_demand=True, env=env)
        right = eval_ast(node.right, value_demand=True, env=env)
        return left / right
    if isinstance(node, Invoke):
        fn = eval_ast(node.func, value_demand=True, env=env)
        args = [eval_ast(arg, value_demand=True, env=env) for arg in node.args]
        return invoke_function(fn, args, env)
    if isinstance(node, Program):
        result = None
        for stmt in node.statements:
            result = eval_ast(stmt, value_demand=True, env=env)
        return result
    if isinstance(node, list):
        return [eval_ast(x, value_demand=True, env=env) for x in node]
    if isinstance(node, tuple):
        raise EnzoRuntimeError(error_message_tuple_ast(node))
    if isinstance(node, BindOrRebind):
        env[node.target] = eval_ast(node.value, value_demand=True, env=env)
        return env[node.target]
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
