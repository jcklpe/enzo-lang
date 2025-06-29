from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, TableAtom, Binding, BindOrRebind, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode, FunctionRef, ListIndex, TableIndex
from src.error_handling import InterpolationParseError, ReturnSignal, EnzoRuntimeError, EnzoTypeError, EnzoParseError
from src.error_messaging import (
    error_message_already_defined,
    error_message_unknown_variable,
    error_message_not_a_function,
    error_message_tuple_ast,
    error_message_unknown_node,
    error_message_unterminated_interpolation,
    error_message_cannot_assign,
    error_message_index_must_be_number,
    error_message_index_must_be_integer,
    error_message_list_index_out_of_range,
    error_message_table_property_not_found,
    error_message_cant_use_string_as_index,
    error_message_index_applies_to_lists
)

_env = {}  # single global environment

class EnzoFunction:
    def __init__(self, params, body, closure_env):
        self.params = params          # list of (name, default)
        self.body = body              # list of AST stmts
        self.closure_env = closure_env.copy()  # captured env for closure

    def __repr__(self):
        # Show only param names for readability
        param_names = [p[0] if isinstance(p, (list, tuple)) else str(p) for p in self.params]
        return f"<function ({', '.join(param_names)}) ...>"

def invoke_function(fn, args, env):
    if not isinstance(fn, EnzoFunction):
        raise EnzoTypeError(error_message_not_a_function(fn), code_line=getattr(fn, 'code_line', None))
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


def eval_ast(node, value_demand=False, already_invoked=False, env=None, src_line=None):
    if env is None:
        env = _env
    if node is None:
        # Ignore empty statements (e.g., from extra semicolons)
        return None
    code_line = getattr(node, 'code_line', None)
    if isinstance(node, NumberAtom):
        return node.value
    if isinstance(node, TextAtom):
        # Pass the original code line to _interp for error reporting
        return _interp(node.value, src_line=code_line)
    if isinstance(node, ListAtom):
        return [eval_ast(el, value_demand=True, env=env) for el in node.elements]
    if isinstance(node, TableAtom):
        return {k: eval_ast(v, value_demand=True, env=env) for k, v in node.items}
    if isinstance(node, Binding):
        name = node.name
        if name in env:
            raise EnzoRuntimeError(error_message_already_defined(name), code_line=node.code_line)
        # Handle empty bind: $x: ;
        if node.value is None:
            env[name] = Empty()
            return None  # Do not output anything for empty bind
        # If value is a FunctionAtom, store as function object, not result
        if isinstance(node.value, FunctionAtom):
            env[name] = EnzoFunction(node.value.params, node.value.body, env)
            return None  # Do not output anything for assignment
        val = eval_ast(node.value, value_demand=False, env=env)  # storage context
        env[name] = val
        return None  # Do not output anything for assignment
    if isinstance(node, VarInvoke):
        name = node.name
        if name not in env:
            raise EnzoRuntimeError(error_message_unknown_variable(name), code_line=node.code_line)
        val = env[name]
        # Demand-value context: invoke if function
        if value_demand and isinstance(val, EnzoFunction):
            return invoke_function(val, [], env)
        return val
    if isinstance(node, FunctionRef):
        name = node.name
        if name not in env:
            raise EnzoRuntimeError(error_message_unknown_variable(name), code_line=node.code_line)
        val = env[name]
        if not isinstance(val, EnzoFunction):
            raise EnzoTypeError(error_message_not_a_function(val), code_line=code_line)
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
        left = eval_ast(node.func, value_demand=True, env=env)
        args = [eval_ast(arg, value_demand=True, env=env) for arg in node.args]
        # List indexing
        if isinstance(left, list):
            if len(args) != 1:
                raise EnzoTypeError(error_message_index_must_be_number(), code_line=getattr(node, 'code_line', None))
            idx = args[0]
            if not isinstance(idx, (int, float)):
                raise EnzoTypeError(error_message_index_must_be_number(), code_line=getattr(node, 'code_line', None))
            if isinstance(idx, float):
                if not idx.is_integer():
                    raise EnzoTypeError(error_message_index_must_be_integer(), code_line=getattr(node, 'code_line', None))
                idx = int(idx)
            if not isinstance(idx, int):
                raise EnzoTypeError(error_message_index_must_be_integer(), code_line=getattr(node, 'code_line', None))
            # 1-based index
            if idx < 1 or idx > len(left):
                raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=getattr(node, 'code_line', None))
            return left[idx - 1]
        # Table property access
        if isinstance(left, dict):
            if len(args) != 1:
                raise EnzoTypeError(error_message_table_property_not_found("<missing key>"), code_line=getattr(node, 'code_line', None))
            key = args[0]
            if not isinstance(key, str):
                raise EnzoTypeError(error_message_table_property_not_found(key), code_line=getattr(node, 'code_line', None))
            if key not in left:
                raise EnzoRuntimeError(error_message_table_property_not_found(key), code_line=getattr(node, 'code_line', None))
            return left[key]
        # Function call
        if isinstance(left, EnzoFunction):
            return invoke_function(left, args, env)
        # Not a list, table, or function
        raise EnzoTypeError(error_message_index_applies_to_lists(), code_line=getattr(node, 'code_line', None))
    if isinstance(node, Program):
        # For a program (file or REPL), output each top-level statement's value (if not None)
        results = []
        for stmt in node.statements:
            if stmt is not None:
                val = eval_ast(stmt, value_demand=True, env=env)
                if val is not None:
                    results.append(val)
        # Print each result on its own line (handled by CLI), or return as list for test runner
        return results
    if isinstance(node, list):
        # For a list of statements (from a single line), only return the last value
        result = None
        for x in node:
            val = eval_ast(x, value_demand=True, env=env)
            result = val
        return result
    if isinstance(node, tuple):
        # Raise a clear error for tuple ASTs
        raise EnzoRuntimeError(error_message_tuple_ast(), code_line=getattr(node, 'code_line', None))
    if isinstance(node, BindOrRebind):
        target = node.target
        value = eval_ast(node.value, value_demand=True, env=env)
        def enzo_type(val):
            if isinstance(val, (int, float)):
                return "Number"
            if isinstance(val, str):
                return "Text"
            if isinstance(val, list):
                return "List"
            if isinstance(val, dict):
                return "Table"
            if isinstance(val, EnzoFunction):
                return "Function"
            if isinstance(val, Empty):
                return "Empty"
            return type(val).__name__
        # Assignment to variable
        if isinstance(target, str):
            name = target
            if name not in env:
                env[name] = value
                return None
            old_val = env[name]
            if not isinstance(old_val, Empty) and enzo_type(old_val) != enzo_type(value):
                raise EnzoRuntimeError(error_message_cannot_assign(enzo_type(value), enzo_type(old_val)), code_line=node.code_line)
            env[name] = value
            return None
        # Assignment to variable via VarInvoke
        if isinstance(target, VarInvoke):
            name = target.name
            t_code_line = getattr(target, 'code_line', node.code_line)
            if name not in env:
                env[name] = value
                return None
            old_val = env[name]
            if not isinstance(old_val, Empty) and enzo_type(old_val) != enzo_type(value):
                raise EnzoRuntimeError(error_message_cannot_assign(enzo_type(value), enzo_type(old_val)), code_line=t_code_line)
            env[name] = value
            return None
        # Assignment to list index
        if isinstance(target, ListIndex):
            base = eval_ast(target.base, env=env)
            idx = eval_ast(target.index, env=env)
            t_code_line = getattr(target, 'code_line', node.code_line)
            if not isinstance(base, list):
                raise EnzoTypeError(error_message_index_applies_to_lists(), code_line=t_code_line)
            if isinstance(idx, str):
                raise EnzoTypeError(error_message_cant_use_string_as_index(), code_line=t_code_line)
            if not isinstance(idx, (int, float)):
                raise EnzoTypeError(error_message_index_must_be_number(), code_line=t_code_line)
            if isinstance(idx, float):
                if not idx.is_integer():
                    raise EnzoTypeError(error_message_index_must_be_integer(), code_line=t_code_line)
                idx = int(idx)
            if not isinstance(idx, int):
                raise EnzoTypeError(error_message_index_must_be_integer(), code_line=t_code_line)
            if idx < 1 or idx > len(base):
                raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
            base[idx - 1] = value
            return None
        # Assignment to table property
        if isinstance(target, TableIndex):
            base = eval_ast(target.base, env=env)
            key = target.key
            t_code_line = getattr(target, 'code_line', node.code_line)
            if isinstance(key, VarInvoke):
                key = eval_ast(key, env=env)
            if not isinstance(base, dict):
                raise EnzoTypeError(error_message_table_property_not_found(key), code_line=t_code_line)
            base[key] = value
            return None
        raise EnzoRuntimeError(error_message_cannot_assign_target(target), code_line=getattr(node, 'code_line', None))
    if isinstance(node, ListIndex):
        base = eval_ast(node.base, env=env)
        idx = eval_ast(node.index, env=env)
        t_code_line = getattr(node, 'code_line', code_line)
        if isinstance(idx, str):
            raise EnzoRuntimeError(error_message_cant_use_string_as_index(), code_line=t_code_line)
        if not isinstance(base, list):
            if isinstance(node.base, (VarInvoke, TableIndex)):
                raise EnzoRuntimeError(error_message_index_applies_to_lists(), code_line=t_code_line)
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        if not isinstance(idx, int) or idx < 1 or idx > len(base):
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        return base[idx - 1]
    if isinstance(node, TableIndex):
        base = eval_ast(node.base, env=env)
        key = node.key
        t_code_line = getattr(node, 'code_line', code_line)
        if isinstance(key, VarInvoke):
            key = eval_ast(key, env=env)
        if isinstance(base, dict):
            # Try both $key and key
            if key in base:
                return base[key]
            if isinstance(key, str) and not key.startswith('$') and ('$' + key) in base:
                return base['$' + key]
            raise EnzoRuntimeError(error_message_table_property_not_found(key), code_line=t_code_line)
        raise EnzoRuntimeError(error_message_table_property_not_found(key), code_line=t_code_line)
    raise EnzoRuntimeError(error_message_unknown_node(node), code_line=getattr(node, 'code_line', None))

# ── text_atom‐interpolation helper ───────────────────────────────────────────
def _interp(s: str, src_line: str = None):
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
                from src.error_messaging import error_message_parse_error_in_interpolation
                # Use the original quoted code line for error reporting
                raise EnzoParseError(error_message_parse_error_in_interpolation(), code_line=src_line)
        out.append(concatenated)
        i = k + 1
    return "".join(out)

# Sentinel for uninitialized/empty binds
class Empty:
    def __repr__(self):
        return "<empty>"
