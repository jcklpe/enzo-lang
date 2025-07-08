from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val, log_debug, EnzoList
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, TableAtom, Binding, BindOrRebind, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode, FunctionRef, ListIndex, TableIndex, ReturnNode, PipelineNode, ParameterDeclaration
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
    error_message_list_property_not_found,
    error_message_cant_use_text_as_index,
    error_message_index_applies_to_lists,
    error_message_cannot_assign_target,
    error_message_cannot_declare_this,
    error_message_multiline_function_requires_return,
    error_message_param_outside_function,
    error_message_too_many_args,
    error_message_arg_type_mismatch,
    error_message_missing_necessary_params
)
import os

_env = {}  # single global environment

class EnzoFunction:
    def __init__(self, params, local_vars, body, closure_env, is_multiline=False):
        self.params = params          # list of (name, default)
        self.local_vars = local_vars  # list of Binding nodes
        self.body = body              # list of AST stmts
        self.closure_env = closure_env.copy()  # captured env for closure
        self.is_multiline = is_multiline      # track if function atom is multiline

    def __repr__(self):
        # Show only param names for readability
        param_names = [p[0] if isinstance(p, (list, tuple)) else str(p) for p in self.params]
        return f"<function ({', '.join(param_names)}) multiline={self.is_multiline}>"

def invoke_function(fn, args, env, self_obj=None):
    if not isinstance(fn, EnzoFunction):
        raise EnzoTypeError(error_message_not_a_function(fn), code_line=getattr(fn, 'code_line', None))

    # 1. Validate argument count
    if len(args) > len(fn.params):
        raise EnzoRuntimeError(error_message_too_many_args())

    # 2. Check for required parameters (those with empty defaults)
    required_param_count = 0
    for param_name, default in fn.params:
        if default is None:  # Empty default means required parameter
            required_param_count += 1
        else:
            break  # Required params must come first

    if len(args) < required_param_count:
        raise EnzoRuntimeError(error_message_missing_necessary_params())

    # 3. Validate argument types against parameter defaults
    for i, arg in enumerate(args):
        param_name, default = fn.params[i]
        expected_type = _infer_type_from_default(default)
        actual_type = _get_enzo_type(arg)

        # Only validate if we can infer the expected type and it doesn't match
        if expected_type and actual_type != expected_type:
            raise EnzoRuntimeError(error_message_arg_type_mismatch(param_name, expected_type, actual_type))

    call_env = fn.closure_env.copy()
    # Bind parameters
    for (param_name, default), arg in zip(fn.params, args):
        call_env[param_name] = arg
    if len(args) < len(fn.params):
        for (param_name, default) in fn.params[len(args):]:
            if default is None:
                # This should never happen since we already checked required params above
                raise EnzoRuntimeError(error_message_missing_necessary_params())
            call_env[param_name] = eval_ast(default, value_demand=True, env=ChainMap(call_env, env))

    # Inject $self if provided
    if self_obj is not None:
        call_env['$self'] = self_obj

    # Create a combined environment that allows both reading from outer env and writing to call_env
    # Make sure we don't pollute the outer environment
    # Function-local variables should shadow global variables, not conflict with them
    combined_env = {}
    combined_env.update(env)  # Add outer environment variables (read-only)
    combined_env.update(call_env)  # Add function parameters

    # For function execution, we need to allow local variables to shadow global ones
    # So we'll use a special binding context that doesn't check for global conflicts

    # Check if multi-line function atom has explicit return
    if getattr(fn, 'is_multiline', False):
        has_return = any(isinstance(stmt, ReturnNode) for stmt in fn.body)
        if not has_return:
            raise EnzoRuntimeError(error_message_multiline_function_requires_return())

    # Execute all statements in order: local_vars are bindings that appeared in the function body
    # and should be executed in the order they appeared relative to other statements
    # For now, we'll execute local_vars first since they're typically at the beginning
    # but this is a limitation of the current parser separation

    try:
        res = None

        # Execute local variables (bindings like $x: 5;)
        for local_var in getattr(fn, 'local_vars', []):
            res = eval_ast(local_var, value_demand=True, env=combined_env, is_function_context=True)

        # Execute body statements (rebinds, returns, etc.)
        for stmt in fn.body:
            res = eval_ast(stmt, value_demand=True, env=combined_env, is_function_context=True)
    except ReturnSignal as ret:
        return ret.value
    return res


def _infer_type_from_default(default_value):
    """Infer expected parameter type from default value AST node."""
    from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, TableAtom

    if isinstance(default_value, NumberAtom):
        return "number"
    elif isinstance(default_value, TextAtom):
        return "text"
    elif isinstance(default_value, ListAtom):
        return "list"
    elif isinstance(default_value, TableAtom):
        return "table"
    # For complex expressions or Empty(), don't enforce type validation
    return None

def _get_enzo_type(value):
    """Get the Enzo type name for a runtime value."""
    if isinstance(value, (int, float)):
        return "number"
    elif isinstance(value, str):
        return "text"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "table"
    elif isinstance(value, EnzoFunction):
        return "function"
    elif isinstance(value, Empty):
        return "empty"
    else:
        return type(value).__name__.lower()


def eval_ast(node, value_demand=False, already_invoked=False, env=None, src_line=None, is_function_context=False):
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
        return _interp(node.value, src_line=code_line, env=env)
    if isinstance(node, ListAtom):
        from src.enzo_parser.ast_nodes import ListKeyValue
        from src.runtime_helpers import EnzoList

        enzo_list = EnzoList()
        for el in node.elements:
            if isinstance(el, ListKeyValue):
                # Key-value pair
                key = el.keyname
                if isinstance(el.value, FunctionAtom):
                    value = eval_ast(el.value, value_demand=False, env=env)
                else:
                    value = eval_ast(el.value, value_demand=True, env=env)
                enzo_list.set_key(key, value)
            else:
                # Regular element - gets auto-indexed
                if isinstance(el, FunctionAtom):
                    value = eval_ast(el, value_demand=False, env=env)
                else:
                    value = eval_ast(el, value_demand=True, env=env)
                enzo_list.append(value)
        return enzo_list
    if isinstance(node, TableAtom):
        tbl = Table((k, eval_ast(v, value_demand=True, env=env)) for k, v in node.items)
        return tbl
    if isinstance(node, Binding):
        name = node.name
        log_debug(f"[BINDING] Attempting to bind {name}, env keys: {list(env.keys())}")
        if name == '$this':
            raise EnzoRuntimeError(error_message_cannot_declare_this(), code_line=node.code_line)
        # In function context, local variables can shadow global ones
        # In global context, redeclaration is an error
        if not is_function_context and name in env:
            raise EnzoRuntimeError(error_message_already_defined(name), code_line=node.code_line)
        # Handle empty bind: $x: ;
        if node.value is None:
            env[name] = Empty()
            return None  # Do not output anything for empty bind
        # If value is a FunctionAtom, store as function object, not result
        if isinstance(node.value, FunctionAtom):
            fn = EnzoFunction(node.value.params, node.value.local_vars, node.value.body, env, getattr(node.value, 'is_multiline', False))
            env[name] = fn
            # For variable bindings, also make accessible with/without $ prefix
            if name.startswith('$'):
                # Make $variable also accessible as bare name
                bare_name = name[1:]  # Remove the $ prefix
                if bare_name not in env:  # Don't overwrite existing bare variable
                    env[bare_name] = fn
            else:
                # Make bare variable also accessible with $ prefix
                dollar_name = '$' + name
                if dollar_name not in env:  # Don't overwrite existing $variable
                    env[dollar_name] = fn
            return None  # Do not output anything for assignment
        val = eval_ast(node.value, value_demand=False, env=env)  # storage context
        env[name] = val
        # For variable bindings, also make accessible with/without $ prefix
        if name.startswith('$'):
            # Make $variable also accessible as bare name
            bare_name = name[1:]  # Remove the $ prefix
            if bare_name not in env:  # Don't overwrite existing bare variable
                env[bare_name] = val
        else:
            # Make bare variable also accessible with $ prefix
            dollar_name = '$' + name
            if dollar_name not in env:  # Don't overwrite existing $variable
                env[dollar_name] = val
        return None  # Do not output anything for assignment
    if isinstance(node, VarInvoke):
        name = node.name
        if name not in env:
            raise EnzoRuntimeError(error_message_unknown_variable(name), code_line=node.code_line)
        val = env[name]
        # Check if this is a function
        if isinstance(val, EnzoFunction):
            # Auto-invoke functions when referenced with $ sigil in value_demand context
            if value_demand:
                # Bare function names (without $ sigil) cannot be auto-invoked
                if not name.startswith('$'):
                    raise EnzoRuntimeError("error: expected function reference (@) or function invocation ($)", code_line=node.code_line)
                return invoke_function(val, [], env, self_obj=None)
        return val
    if isinstance(node, FunctionRef):
        # Evaluate the expression to get the function object
        val = eval_ast(node.expr, value_demand=False, env=env)
        if not isinstance(val, EnzoFunction):
            raise EnzoTypeError(error_message_not_a_function(val), code_line=node.code_line)
        return val
    if isinstance(node, FunctionAtom):
        # Demand-value context: invoke
        if value_demand:
            fn = EnzoFunction(node.params, node.local_vars, node.body, env, getattr(node, 'is_multiline', False))
            return invoke_function(fn, [], env, self_obj=None)
        else:
            return EnzoFunction(node.params, node.local_vars, node.body, env, getattr(node, 'is_multiline', False))
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
        left = eval_ast(node.func, value_demand=False, env=env)  # Get function object, don't invoke it yet
        args = [eval_ast(arg, value_demand=True, env=env) for arg in node.args]

        # EnzoList indexing and keyed access
        from src.runtime_helpers import EnzoList
        if isinstance(left, EnzoList):
            if len(args) != 1:
                raise EnzoTypeError(error_message_index_must_be_number(), code_line=getattr(node, 'code_line', None))
            key = args[0]
            try:
                # Try index access first (if it's a number)
                if isinstance(key, (int, float)):
                    if isinstance(key, float) and not key.is_integer():
                        raise EnzoTypeError(error_message_index_must_be_integer(), code_line=getattr(node, 'code_line', None))
                    idx = int(key)
                    return left.get_by_index(idx)
                # Try key access (if it's a string)
                elif isinstance(key, str):
                    return left.get_by_key(key)
                else:
                    raise EnzoTypeError(error_message_index_must_be_number(), code_line=getattr(node, 'code_line', None))
            except IndexError:
                raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=getattr(node, 'code_line', None))
            except KeyError:
                raise EnzoRuntimeError(error_message_list_property_not_found(key), code_line=getattr(node, 'code_line', None))

        # Legacy list indexing (for backward compatibility)
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
                raise EnzoTypeError(error_message_list_property_not_found("<missing key>"), code_line=getattr(node, 'code_line', None))
            key = args[0]
            if not isinstance(key, str):
                raise EnzoTypeError(error_message_list_property_not_found(key), code_line=getattr(node, 'code_line', None))
            if key not in left:
                raise EnzoRuntimeError(error_message_list_property_not_found(key), code_line=getattr(node, 'code_line', None))
            return left[key]
        # Function call
        if isinstance(left, EnzoFunction):
            # Check if this function call is from property access (e.g., $obj.method())
            self_obj = None
            if isinstance(node.func, TableIndex):
                # Get the base object for $self
                self_obj = eval_ast(node.func.base, env=env)
            return invoke_function(left, args, env, self_obj=self_obj)
        # Not a list, table, or function
        raise EnzoTypeError(error_message_index_applies_to_lists(), code_line=getattr(node, 'code_line', None))
    if isinstance(node, Program):
        # For a program (file or REPL), output each top-level statement's value (if not None)
        results = []
        for stmt in node.statements:
            if stmt is not None:
                try:
                    val = eval_ast(stmt, value_demand=True, env=env)
                    if val is not None:
                        results.append(val)
                except Exception as e:
                    # Format the error as string, as the test runner expects error output
                    results.append(str(e))
                    break  # Stop evaluating further statements after the first error
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
    if isinstance(node, ReturnNode):
        val = eval_ast(node.value, value_demand=True, env=env)
        raise ReturnSignal(val)
    if isinstance(node, PipelineNode):
        # Evaluate the left side (the value to pipe)
        left_val = eval_ast(node.left, value_demand=True, env=env)
        # Evaluate the right side
        right_expr = node.right
        # Create a new environment with $this bound to the left value
        pipeline_env = env.copy()
        pipeline_env['$this'] = left_val

        # If right side is a FunctionAtom, invoke it directly
        if isinstance(right_expr, FunctionAtom):
            fn = EnzoFunction(right_expr.params, right_expr.local_vars, right_expr.body, pipeline_env, getattr(right_expr, 'is_multiline', False))
            return invoke_function(fn, [], pipeline_env, self_obj=None)
        # For expressions that can potentially reference $this, evaluate in pipeline environment
        elif isinstance(right_expr, (AddNode, SubNode, MulNode, DivNode, VarInvoke, Invoke, TextAtom, ListIndex, TableIndex)):
            return eval_ast(right_expr, value_demand=True, env=pipeline_env)
        else:
            # For literals and other nodes that can't reference $this, this doesn't make sense
            raise EnzoRuntimeError("error: pipeline expects function atom after `then`", code_line=getattr(node, 'code_line', None))
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

            # Handle EnzoList assignment
            from src.runtime_helpers import EnzoList
            if isinstance(base, EnzoList):
                if isinstance(idx, (int, float)):
                    if isinstance(idx, float) and not idx.is_integer():
                        raise EnzoTypeError(error_message_index_must_be_integer(), code_line=t_code_line)
                    try:
                        # For EnzoList, use 0-based indexing internally but convert from 1-based
                        base[int(idx) - 1] = value
                        return None
                    except IndexError:
                        raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
                else:
                    raise EnzoTypeError(error_message_index_must_be_number(), code_line=t_code_line)

            # Legacy list handling
            if not isinstance(base, list):
                raise EnzoTypeError(error_message_index_applies_to_lists(), code_line=t_code_line)
            if isinstance(idx, str):
                raise EnzoTypeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
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
            property_name = target.key
            t_code_line = getattr(target, 'code_line', node.code_line)
            if isinstance(property_name, VarInvoke):
                property_name = eval_ast(property_name, env=env)

            # Handle EnzoList property assignment
            from src.runtime_helpers import EnzoList
            if isinstance(base, EnzoList):
                try:
                    base.set_by_key(property_name, value)
                    return None
                except KeyError:
                    raise EnzoRuntimeError(error_message_list_property_not_found(property_name), code_line=t_code_line)

            # Legacy table handling
            # Ensure base is a dict or Table (which is a dict subclass)
            if not isinstance(base, dict):
                raise EnzoTypeError(error_message_list_property_not_found(property_name), code_line=t_code_line)
            # Overwrite the property value (dict assignment always overwrites)
            # --- FIX: Use $property if present, else try $property ---
            found = False
            if property_name in base:
                base[property_name] = value
                found = True
            elif isinstance(property_name, str) and not property_name.startswith('$') and ('$' + property_name) in base:
                base['$' + property_name] = value
                found = True
            if not found:
                raise EnzoRuntimeError(error_message_list_property_not_found(property_name), code_line=t_code_line)
            log_debug(f"[Table property rebind] property: {property_name} | table after: {base!r}")
            return None
        raise EnzoRuntimeError(error_message_cannot_assign_target(target), code_line=getattr(node, 'code_line', None))
    if isinstance(node, ListIndex):
        base = eval_ast(node.base, env=env)
        idx = eval_ast(node.index, env=env)
        t_code_line = getattr(node, 'code_line', code_line)

        # Handle EnzoList indexing
        from src.runtime_helpers import EnzoList
        if isinstance(base, EnzoList):
            try:
                if isinstance(idx, (int, float)):
                    if isinstance(idx, float) and not idx.is_integer():
                        raise EnzoTypeError(error_message_index_must_be_integer(), code_line=t_code_line)
                    return base.get_by_index(int(idx))
                else:
                    raise EnzoTypeError(error_message_index_must_be_number(), code_line=t_code_line)
            except IndexError:
                raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)

        # Legacy list handling
        if isinstance(idx, str):
            raise EnzoRuntimeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
        if not isinstance(base, list):
            if isinstance(node.base, (VarInvoke, TableIndex)):
                raise EnzoRuntimeError(error_message_index_applies_to_lists(), code_line=t_code_line)
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        if not isinstance(idx, int) or idx < 1 or idx > len(base):
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        return base[idx - 1]
    if isinstance(node, TableIndex):
        base = eval_ast(node.base, env=env)
        property_name = node.key
        t_code_line = getattr(node, 'code_line', code_line)

        if isinstance(property_name, VarInvoke):
            property_name = eval_ast(property_name, env=env)

        # Handle EnzoList property access
        from src.runtime_helpers import EnzoList
        if isinstance(base, EnzoList):
            try:
                return base.get_by_key(property_name)
            except KeyError:
                raise EnzoRuntimeError(error_message_list_property_not_found(property_name), code_line=t_code_line)

        # Legacy table handling
        if isinstance(base, dict):
            # Try both $property and property
            if property_name in base:
                return base[property_name]
            if isinstance(property_name, str) and not property_name.startswith('$') and ('$' + property_name) in base:
                return base['$' + property_name]
            raise EnzoRuntimeError(error_message_list_property_not_found(property_name), code_line=t_code_line)
        raise EnzoRuntimeError(error_message_list_property_not_found(property_name), code_line=t_code_line)
    if isinstance(node, ParameterDeclaration):
        raise EnzoRuntimeError(error_message_param_outside_function(), code_line=getattr(node, 'code_line', None))
    raise EnzoRuntimeError(error_message_unknown_node(node), code_line=getattr(node, 'code_line', None))

# ── text_atom‐interpolation helper ───────────────────────────────────────────
def _interp(s: str, src_line: str = None, env=None):
    # Given a Python string `s`, expand each "<expr>" by:
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
                val = eval_ast(expr_ast, value_demand=True, env=env)
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
    def __repr__(self):
        return "<empty>"
        return "<empty>"
