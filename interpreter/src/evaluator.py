from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val, log_debug, EnzoList, deep_copy_enzo_value
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, Binding, BindOrRebind, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode, FunctionRef, ListIndex, ReturnNode, PipelineNode, ParameterDeclaration, ReferenceAtom
from src.error_handling import InterpolationParseError, ReturnSignal, EnzoRuntimeError, EnzoTypeError, EnzoParseError
from src.error_messaging import (
    error_message_already_defined,
    error_message_unknown_variable,
    error_message_not_a_function,
    error_message_tuple_ast,
    error_message_unknown_node,
    error_message_unterminated_interpolation,
    error_message_cannot_bind,
    error_message_index_must_be_number,
    error_message_index_must_be_integer,
    error_message_list_index_out_of_range,
    error_message_list_property_not_found,
    error_message_cant_use_text_as_index,
    error_message_index_applies_to_lists,
    error_message_cannot_bind_target,
    error_message_cannot_declare_this,
    error_message_multiline_function_requires_return,
    error_message_param_outside_function,
    error_message_too_many_args,
    error_message_arg_type_mismatch,
    error_message_missing_necessary_params,
    error_message_cannot_reference_this_in_named_function
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

class ReferenceWrapper:
    """Wrapper for explicit references created with @ operator."""
    def __init__(self, expr, env):
        self.expr = expr  # The AST expression to evaluate for the reference
        self.env = env    # The environment where the reference was created

    def get_value(self):
        """Get the current value of the referenced expression."""
        return eval_ast(self.expr, value_demand=True, env=self.env)

    def get_target_info(self):
        """Get information about the reference target for assignment."""
        return self.expr, self.env

    def set_value(self, value):
        """Set the value of the referenced target."""
        if isinstance(self.expr, VarInvoke):
            var_name = self.expr.name
            if var_name in self.env:
                self.env[var_name] = value
                # Handle variable mirroring
                if var_name.startswith('$'):
                    bare_name = var_name[1:]
                    if bare_name in self.env:
                        self.env[bare_name] = value
                else:
                    dollar_name = '$' + var_name
                    if dollar_name in self.env:
                        self.env[dollar_name] = value
        elif isinstance(self.expr, ListIndex):
            # Handle list property assignment through reference
            base_val = eval_ast(self.expr.base, value_demand=True, env=self.env)
            if self.expr.is_property_access:
                if isinstance(base_val, EnzoList):
                    base_val.set_by_key(self.expr.index.value, value)
                elif isinstance(base_val, dict):
                    base_val[self.expr.index.value] = value
            else:
                index = eval_ast(self.expr.index, value_demand=True, env=self.env)
                if isinstance(base_val, EnzoList):
                    base_val[int(index) - 1] = value  # 1-based indexing
                else:
                    base_val[int(index) - 1] = value

    def __repr__(self):
        return f"<reference to {self.expr}>"

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
    # Bind parameters with copy-by-default semantics
    for (param_name, default), arg in zip(fn.params, args):
        # Handle reference vs copy semantics for function arguments
        if isinstance(arg, ReferenceWrapper):
            # This is an explicit reference (@variable), store the reference wrapper
            call_env[param_name] = arg
        else:
            # Copy-by-default: make a deep copy of the argument
            call_env[param_name] = deep_copy_enzo_value(arg)
    if len(args) < len(fn.params):
        for (param_name, default) in fn.params[len(args):]:
            if default is None:
                # This should never happen since we already checked required params above
                raise EnzoRuntimeError(error_message_missing_necessary_params())
            default_val = eval_ast(default, value_demand=True, env=ChainMap(call_env, env))
            # Default values are also copied
            call_env[param_name] = deep_copy_enzo_value(default_val)

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
    from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom

    if isinstance(default_value, NumberAtom):
        return "number"
    elif isinstance(default_value, TextAtom):
        return "text"
    elif isinstance(default_value, ListAtom):
        return "list"
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
            # Evaluate the FunctionAtom to trigger validation (e.g., $this checks)
            fn = eval_ast(node.value, value_demand=False, env=env, is_function_context=is_function_context)
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
            return None  # Do not output anything for binding
        val = eval_ast(node.value, value_demand=False, env=env)  # storage context

        # Handle reference vs copy semantics for bindings
        if isinstance(val, ReferenceWrapper):
            # This is an explicit reference (@variable), store the reference wrapper
            actual_val = val
        else:
            # Copy-by-default: make a deep copy of the value
            actual_val = deep_copy_enzo_value(val)

        env[name] = actual_val
        # For variable bindings, also make accessible with/without $ prefix
        if name.startswith('$'):
            # Make $variable also accessible as bare name
            bare_name = name[1:]  # Remove the $ prefix
            if bare_name not in env:  # Don't overwrite existing bare variable
                env[bare_name] = actual_val
        else:
            # Make bare variable also accessible with $ prefix
            dollar_name = '$' + name
            if dollar_name not in env:  # Don't overwrite existing $variable
                env[dollar_name] = actual_val
        return None  # Do not output anything for binding
    if isinstance(node, VarInvoke):
        name = node.name
        if name not in env:
            raise EnzoRuntimeError(error_message_unknown_variable(name), code_line=node.code_line)
        val = env[name]

        # Handle reference wrapper: return the current value of the reference
        if isinstance(val, ReferenceWrapper):
            referenced_val = val.get_value()
            # Check if the referenced value is a function
            if isinstance(referenced_val, EnzoFunction):
                # Auto-invoke functions when referenced with $ sigil in value_demand context
                if value_demand:
                    if not name.startswith('$'):
                        raise EnzoRuntimeError("error: expected function reference (@) or function invocation ($)", code_line=node.code_line)
                    return invoke_function(referenced_val, [], env, self_obj=None)
            return referenced_val

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
    if isinstance(node, ReferenceAtom):
        target = node.target

        # Special handling for function references (backwards compatibility)
        if isinstance(target, VarInvoke):
            # Check if the target is a function
            var_name = target.name
            if var_name in env:
                var_value = env[var_name]
                if isinstance(var_value, EnzoFunction):
                    return var_value  # Return function directly for @function
        elif isinstance(target, ListIndex) and target.is_property_access:
            # Handle @object.method
            try:
                from src.runtime_helpers import EnzoList
                base_val = eval_ast(target.base, value_demand=True, env=env)
                if isinstance(base_val, EnzoList):
                    prop_name = target.index.value
                    prop_val = base_val.get_by_key(prop_name)
                    if isinstance(prop_val, EnzoFunction):
                        return prop_val  # Return function directly for @object.method
                elif isinstance(base_val, dict):
                    prop_name = target.index.value
                    prop_val = base_val.get(prop_name)
                    if isinstance(prop_val, EnzoFunction):
                        return prop_val
            except Exception as e:
                # If we can't access the property, fall through to ReferenceWrapper
                pass

        # For non-function references, create ReferenceWrapper
        return ReferenceWrapper(target, env)
    if isinstance(node, FunctionAtom):
        # Check if this is a named function that references $this
        if getattr(node, 'is_named', False):
            # Check all statements in the function body for $this references
            for stmt in node.body:
                if _check_for_this_reference(stmt):
                    raise EnzoRuntimeError(error_message_cannot_reference_this_in_named_function(), code_line=node.code_line)

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

        # If left is a ReferenceWrapper that refers to a function, dereference it
        if isinstance(left, ReferenceWrapper):
            left = left.get_value()

        # Evaluate arguments, but preserve ReferenceWrapper objects for function calls
        args = []
        for arg in node.args:
            arg_result = eval_ast(arg, value_demand=False, env=env)  # Don't dereference yet
            if isinstance(arg_result, ReferenceWrapper):
                # Keep the ReferenceWrapper for the function call
                args.append(arg_result)
            else:
                # For non-references, evaluate normally
                args.append(eval_ast(arg, value_demand=True, env=env))

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
        # Function invocation
        if isinstance(left, EnzoFunction):
            # Check if this function invocation is from property access (e.g., $obj.method())
            self_obj = None
            if isinstance(node.func, ListIndex) and getattr(node.func, 'is_property_access', False):
                # This is a method invocation - get the base object for $self
                self_obj = eval_ast(node.func.base, env=env)
            return invoke_function(left, args, env, self_obj=self_obj)
        # Not a list or function
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
        pipeline_env['this'] = left_val  # Also make available without $ prefix for @this

        # If right side is a FunctionAtom, invoke it directly
        if isinstance(right_expr, FunctionAtom):
            fn = EnzoFunction(right_expr.params, right_expr.local_vars, right_expr.body, pipeline_env, getattr(right_expr, 'is_multiline', False))
            return invoke_function(fn, [], pipeline_env, self_obj=None)
        # For expressions that can potentially reference $this, evaluate in pipeline environment
        elif isinstance(right_expr, (AddNode, SubNode, MulNode, DivNode, VarInvoke, Invoke, TextAtom, ListIndex, ReferenceAtom)):
            return eval_ast(right_expr, value_demand=True, env=pipeline_env)
        else:
            # For literals and other nodes that can't reference $this, this doesn't make sense
            raise EnzoRuntimeError("error: pipeline expects function atom after `then`", code_line=getattr(node, 'code_line', None))
    if isinstance(node, BindOrRebind):
        target = node.target
        value = eval_ast(node.value, value_demand=True, env=env)

        # Handle reference vs copy semantics
        if isinstance(value, ReferenceWrapper):
            # This is an explicit reference (@variable), store the reference wrapper
            actual_value = value
        else:
            # Copy-by-default: make a deep copy of the value
            actual_value = deep_copy_enzo_value(value)

        def enzo_type(val):
            if isinstance(val, ReferenceWrapper):
                # For type checking, look at the referenced value
                referenced_val = val.get_value()
                return enzo_type(referenced_val)
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
                env[name] = actual_value
                return None
            old_val = env[name]
            if not isinstance(old_val, Empty) and enzo_type(old_val) != enzo_type(actual_value):
                raise EnzoRuntimeError(error_message_cannot_bind(enzo_type(actual_value), enzo_type(old_val)), code_line=node.code_line)
            env[name] = actual_value
            return None
        # Assignment to variable via VarInvoke
        if isinstance(target, VarInvoke):
            name = target.name
            t_code_line = getattr(target, 'code_line', node.code_line)
            if name not in env:
                env[name] = actual_value
                return None
            old_val = env[name]

            # Special case: if the target variable contains a ReferenceWrapper,
            # we need to update the original referenced variable
            if isinstance(old_val, ReferenceWrapper):
                # Get the target expression and environment from the reference
                ref_expr, ref_env = old_val.get_target_info()

                # Handle assignment to the referenced variable
                if isinstance(ref_expr, VarInvoke):
                    # Simple variable reference: update the original variable
                    ref_name = ref_expr.name
                    if ref_name in ref_env:
                        ref_old_val = ref_env[ref_name]
                        if not isinstance(ref_old_val, Empty) and enzo_type(ref_old_val) != enzo_type(actual_value):
                            raise EnzoRuntimeError(error_message_cannot_bind(enzo_type(actual_value), enzo_type(ref_old_val)), code_line=t_code_line)
                        ref_env[ref_name] = actual_value

                        # Also update the mirrored variable name (with/without $ prefix)
                        if ref_name.startswith('$'):
                            bare_name = ref_name[1:]
                            if bare_name in ref_env:
                                ref_env[bare_name] = actual_value
                        else:
                            dollar_name = '$' + ref_name
                            if dollar_name in ref_env:
                                ref_env[dollar_name] = actual_value

                        return None
                    else:
                        raise EnzoRuntimeError(error_message_unknown_variable(ref_name), code_line=t_code_line)
                else:
                    # Complex reference (e.g., to list index) - not implemented yet
                    raise EnzoRuntimeError("Cannot assign to complex reference", code_line=t_code_line)

            # Normal variable assignment
            if not isinstance(old_val, Empty) and enzo_type(old_val) != enzo_type(actual_value):
                raise EnzoRuntimeError(error_message_cannot_bind(enzo_type(actual_value), enzo_type(old_val)), code_line=t_code_line)
            env[name] = actual_value
            return None
        # Binding to list index
        if isinstance(target, ListIndex):
            # Evaluate the base, but don't dereference ReferenceWrappers yet
            base_result = eval_ast(target.base, env=env, value_demand=False)

            # If the base is a ReferenceWrapper, we need to operate on the referenced object
            if isinstance(base_result, ReferenceWrapper):
                base = base_result.get_value()
                is_reference = True
            else:
                base = base_result
                is_reference = False

            idx = eval_ast(target.index, env=env)
            t_code_line = getattr(target, 'code_line', node.code_line)

            # Determine the value to assign: copy vs reference
            if isinstance(value, ReferenceWrapper):
                assign_value = value.get_value()  # Dereference for assignment
            else:
                assign_value = value  # Use the copied value (from above)

            # Handle EnzoList binding
            from src.runtime_helpers import EnzoList
            if isinstance(base, EnzoList):
                if isinstance(idx, (int, float)):
                    if isinstance(idx, float) and not idx.is_integer():
                        raise EnzoTypeError(error_message_index_must_be_integer(), code_line=t_code_line)
                    try:
                        # For EnzoList, use 0-based indexing internally but convert from 1-based
                        base[int(idx) - 1] = assign_value
                        return None
                    except IndexError:
                        raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
                elif isinstance(idx, str):
                    # Check if this is property access or string indexing
                    if getattr(target, 'is_property_access', False):
                        # Property binding (e.g., $list.name := value)
                        try:
                            base.set_by_key(idx, assign_value)
                            return None
                        except KeyError:
                            raise EnzoRuntimeError(error_message_list_property_not_found(idx), code_line=t_code_line)
                    else:
                        # String indexing binding should error
                        raise EnzoTypeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
                else:
                    raise EnzoTypeError(error_message_index_must_be_number(), code_line=t_code_line)

            # Legacy list handling and property binding on non-EnzoList objects
            if isinstance(idx, str):
                if getattr(target, 'is_property_access', False):
                    # Property binding on non-list objects should give "list property not found"
                    raise EnzoRuntimeError(error_message_list_property_not_found(idx), code_line=t_code_line)
                else:
                    # String indexing binding should error
                    raise EnzoTypeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
            if not isinstance(base, list):
                raise EnzoTypeError(error_message_index_applies_to_lists(), code_line=t_code_line)
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
        raise EnzoRuntimeError(error_message_cannot_bind_target(target), code_line=getattr(node, 'code_line', None))
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
                    val = base.get_by_index(int(idx))
                    # Auto-invoke functions in value demand context
                    if value_demand and isinstance(val, EnzoFunction):
                        return invoke_function(val, [], env, self_obj=None)
                    return val
                elif isinstance(idx, str):
                    # Check if this is property access (.foo) or string indexing (."foo")
                    if getattr(node, 'is_property_access', False):
                        # Property access (e.g., $list.name)
                        val = base.get_by_key(idx)
                        # Auto-invoke functions in value demand context
                        if value_demand and isinstance(val, EnzoFunction):
                            return invoke_function(val, [], env, self_obj=base)
                        return val
                    else:
                        # String indexing like ."foo" should error
                        raise EnzoTypeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
                else:
                    raise EnzoTypeError(error_message_index_must_be_number(), code_line=t_code_line)
            except (IndexError, KeyError):
                if isinstance(idx, str) and getattr(node, 'is_property_access', False):
                    raise EnzoRuntimeError(error_message_list_property_not_found(idx), code_line=t_code_line)
                else:
                    raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)

        # Legacy list handling and property access on non-EnzoList objects
        if isinstance(idx, str):
            if getattr(node, 'is_property_access', False):
                # Property access on non-list objects should give "list property not found"
                raise EnzoRuntimeError(error_message_list_property_not_found(idx), code_line=t_code_line)
            else:
                # String indexing should give "can't use text as index"
                raise EnzoRuntimeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
        if not isinstance(base, list):
            if isinstance(node.base, VarInvoke):
                raise EnzoRuntimeError(error_message_index_applies_to_lists(), code_line=t_code_line)
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        if not isinstance(idx, int) or idx < 1 or idx > len(base):
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        val = base[idx - 1]
        # Auto-invoke functions in value demand context
        if value_demand and isinstance(val, EnzoFunction):
            return invoke_function(val, [], env, self_obj=None)
        return val
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

def _check_for_this_reference(node):
    """Recursively check if any VarInvoke node references $this"""
    if isinstance(node, VarInvoke) and node.name == '$this':
        return True

    # Check all attributes that might contain AST nodes
    for attr_name in dir(node):
        if attr_name.startswith('_'):
            continue
        attr_value = getattr(node, attr_name)

        # Check lists of nodes
        if isinstance(attr_value, list):
            for item in attr_value:
                if hasattr(item, '__class__') and hasattr(item, 'code_line'):  # Likely an AST node
                    if _check_for_this_reference(item):
                        return True

        # Check single nodes
        elif hasattr(attr_value, '__class__') and hasattr(attr_value, 'code_line'):  # Likely an AST node
            if _check_for_this_reference(attr_value):
                return True

    return False
