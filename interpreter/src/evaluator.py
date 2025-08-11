from src.enzo_parser.parser import parse
from src.runtime_helpers import Table, format_val, log_debug, EnzoList, deep_copy_enzo_value
from collections import ChainMap
from src.enzo_parser.ast_nodes import NumberAtom, TextAtom, ListAtom, Binding, BindOrRebind, Invoke, FunctionAtom, Program, VarInvoke, AddNode, SubNode, MulNode, DivNode, ModNode, FunctionRef, ListIndex, ReturnNode, PipelineNode, ParameterDeclaration, ReferenceAtom, BlueprintAtom, BlueprintInstantiation, BlueprintComposition, VariantGroup, VariantGroupExtension, VariantAccess, VariantInstantiation, DestructuringBinding, ReverseDestructuring, ReferenceDestructuring, RestructuringBinding, IfStatement, ComparisonExpression, LogicalExpression, NotExpression, LoopStatement, EndLoopStatement, RestartLoopStatement, ListKeyValue, ListInterpolation
from src.error_handling import InterpolationParseError, ReturnSignal, EnzoRuntimeError, EnzoTypeError, EnzoParseError

# Loop control signals
class EndLoopSignal(Exception):
    def __init__(self, last_result=None):
        self.last_result = last_result

class RestartLoopSignal(Exception):
    def __init__(self, last_result=None):
        self.last_result = last_result
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
    error_message_destructure_count_mismatch,
    error_message_duplicate_variable_names,
    error_message_cannot_declare_this,
    error_message_multiline_function_requires_return,
    error_message_param_outside_function,
    error_message_too_many_args,
    error_message_arg_type_mismatch,
    error_message_missing_necessary_params,
    error_message_cannot_reference_this_in_named_function,
    error_message_for_loop_non_iterable
)
import os

_env = {
    # Predefined type names for use in blueprint definitions and parameter annotations
    'Number': 'Number',
    'Text': 'Text',
    '$self': '$self'
}  # single global environment

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

class EnzoVariantInstance:
    def __init__(self, group_name, variant_name):
        self.group_name = group_name
        self.variant_name = variant_name

    def __repr__(self):
        return f"{self.group_name}.{self.variant_name}"

    def __eq__(self, other):
        if not isinstance(other, EnzoVariantInstance):
            return False
        return self.group_name == other.group_name and self.variant_name == other.variant_name

    def __hash__(self):
        return hash((self.group_name, self.variant_name))

class EnzoVariantGroup:
    def __init__(self, name, variants, group_blueprint=None):
        self.name = name
        self.variants = set(variants)  # Valid variant names
        self.group_blueprint = group_blueprint  # Blueprint for group.group access

    def __str__(self):
        return self.name  # Display just the name, not "VariantGroup(name)"

    def __repr__(self):
        return f"VariantGroup({self.name})"

# Initialize built-in variant groups
def _initialize_builtin_variants():
    """Initialize built-in variant groups for boolean-like values"""
    # Simple boolean-like variants
    _env["True"] = EnzoVariantGroup("True", ["True"])
    _env["False"] = EnzoVariantGroup("False", ["False"])

    # Status variants for more complex boolean logic
    _env["Status"] = EnzoVariantGroup("Status", ["True", "False"])

# Initialize built-ins after the class is defined
_initialize_builtin_variants()

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

class ListElementReference:
    """Reference wrapper for list elements in for loops with @ syntax."""
    def __init__(self, source_list, index):
        self.source_list = source_list  # The original list
        self.index = index  # The index in the list

    def get_value(self):
        """Get the current value of the list element."""
        if isinstance(self.source_list, EnzoList):
            return self.source_list[self.index]
        else:
            return self.source_list[self.index]

    def set_value(self, value):
        """Set the value of the list element."""
        if isinstance(self.source_list, EnzoList):
            self.source_list[self.index] = value
        else:
            self.source_list[self.index] = value

    def __repr__(self):
        return f"<reference to list element {self.index}>"

def invoke_function(fn, args, env, self_obj=None, is_loop_context=False):
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
            default_val = eval_ast(default, value_demand=True, env=ChainMap(call_env, env), is_loop_context=is_loop_context)
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

    # Multi-line function atoms no longer require explicit returns - they return the last evaluated expression

    # Execute all statements in order: local_vars are bindings that appeared in the function body
    # and should be executed in the order they appeared relative to other statements
    # For now, we'll execute local_vars first since they're typically at the beginning
    # but this is a limitation of the current parser separation

    try:
        res = None

        # Execute local variables (bindings like $x: 5;)
        for local_var in getattr(fn, 'local_vars', []):
            res = eval_ast(local_var, value_demand=True, env=combined_env, is_function_context=True, is_loop_context=is_loop_context)

        # Execute body statements (rebinds, returns, etc.)
        for stmt in fn.body:
            res = eval_ast(stmt, value_demand=True, env=combined_env, is_function_context=True, is_loop_context=is_loop_context)
    except ReturnSignal as ret:
        return ret.value
    except (EndLoopSignal, RestartLoopSignal) as loop_signal:
        # For loop control signals, return the last result before re-raising
        # This ensures that expressions before end-loop/restart-loop are captured
        if res is not None:
            # Store the result for the calling loop to collect
            loop_signal.last_result = res
        raise
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


def eval_ast(node, value_demand=False, already_invoked=False, env=None, src_line=None, is_function_context=False, outer_env=None, loop_locals=None, is_loop_context=False):
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
            elif isinstance(el, ListInterpolation):
                # List interpolation: evaluate expression and expand if it's a list
                interpolated_value = eval_ast(el.expression, value_demand=True, env=env)

                if isinstance(interpolated_value, EnzoList):
                    # Check if this is a blueprint instance - don't interpolate blueprint instances
                    if getattr(interpolated_value, '_is_blueprint_instance', False):
                        raise EnzoRuntimeError("error: cannot interpolate non-List into a List", code_line=getattr(el, 'code_line', None))

                    # Expand the list contents into this list
                    for item in interpolated_value._elements:
                        enzo_list.append(item)
                else:
                    # Non-list value: raise error as per test expectations
                    raise EnzoRuntimeError("error: cannot interpolate non-List into a List", code_line=getattr(el, 'code_line', None))
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

        # Special handling for variant group extension
        if name in env and isinstance(node.value, VariantGroup):
            existing_value = env[name]
            if isinstance(existing_value, EnzoVariantGroup):
                # This is extending an existing variant group - merge the variants
                new_variant_group = eval_ast(node.value, value_demand=False, env=env, is_function_context=is_function_context)
                if isinstance(new_variant_group, EnzoVariantGroup):
                    # Merge the variants from both groups
                    merged_variants = existing_value.variants.union(new_variant_group.variants)
                    # Create a new variant group with merged variants
                    merged_group = EnzoVariantGroup(name, list(merged_variants), existing_value.group_blueprint)
                    env[name] = merged_group
                    return None

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

        # Track this variable as a loop-local shadow if we're in a loop context
        if loop_locals is not None:
            loop_locals.add(name)

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
        return None  # Do not output anything for binding    # Handle destructuring statements
    if isinstance(node, DestructuringBinding):
        # Handle basic destructuring: $var1, $var2: source[]

        # Check for duplicate variable names
        seen_vars = set()
        for var_name in node.target_vars:
            if var_name in seen_vars:
                raise EnzoRuntimeError(error_message_duplicate_variable_names(), code_line=node.code_line)
            seen_vars.add(var_name)

        source_value = eval_ast(node.source_expr, value_demand=True, env=env)

        # If source_value is a ReferenceWrapper, dereference it first
        if isinstance(source_value, ReferenceWrapper):
            source_value = source_value.get_value()

            # If the referenced value is a BlueprintInstantiation, evaluate it to get the list
            if isinstance(source_value, BlueprintInstantiation):
                source_value = eval_ast(source_value, value_demand=True, env=env)

        # Check if this is an EnzoList (enhanced list with key support)
        if isinstance(source_value, EnzoList):
            # Try named destructuring first (if variable names match keys)
            named_matches = 0
            for var_name in node.target_vars:
                # Try both with and without $ prefix
                key_candidates = [var_name]
                if var_name.startswith('$'):
                    key_candidates.append(var_name[1:])  # without $
                else:
                    key_candidates.append('$' + var_name)  # with $

                # Check if any key candidate exists in the list
                for key_candidate in key_candidates:
                    try:
                        source_value.get_by_key(key_candidate)
                        named_matches += 1
                        break
                    except KeyError:
                        continue

            # If most/all variables have matching keys, use named destructuring
            if named_matches >= len(node.target_vars) * 0.5:  # At least 50% match
                # Named destructuring
                for var_name in node.target_vars:
                    value = Empty()  # Default if not found

                    # Try both with and without $ prefix
                    key_candidates = [var_name]
                    if var_name.startswith('$'):
                        key_candidates.append(var_name[1:])  # without $
                    else:
                        key_candidates.append('$' + var_name)  # with $

                    # Look for the key
                    for key_candidate in key_candidates:
                        try:
                            value = source_value.get_by_key(key_candidate)
                            break
                        except KeyError:
                            continue

                    env[var_name] = deep_copy_enzo_value(value)

                    # Also make accessible with/without $ prefix
                    if var_name.startswith('$'):
                        bare_name = var_name[1:]
                        if bare_name not in env:
                            env[bare_name] = deep_copy_enzo_value(value)
                    else:
                        dollar_name = '$' + var_name
                        if dollar_name not in env:
                            env[dollar_name] = deep_copy_enzo_value(value)

                return None

            # Fall back to positional destructuring for EnzoList
            items = source_value._elements
        elif isinstance(source_value, list):
            items = source_value
        elif isinstance(source_value, dict):
            items = list(source_value.values())
        else:
            raise EnzoRuntimeError(f"Cannot destructure non-list value: {source_value}", code_line=node.code_line)

        # Positional destructuring (original logic)
        # Check that we have enough elements
        if len(items) < len(node.target_vars):
            raise EnzoRuntimeError(error_message_destructure_count_mismatch(), code_line=node.code_line)

        # Assign each variable
        for i, var_name in enumerate(node.target_vars):
            value = items[i] if i < len(items) else Empty()
            env[var_name] = deep_copy_enzo_value(value)

            # Also make accessible with/without $ prefix
            if var_name.startswith('$'):
                bare_name = var_name[1:]
                if bare_name not in env:
                    env[bare_name] = deep_copy_enzo_value(value)
            else:
                dollar_name = '$' + var_name
                if dollar_name not in env:
                    env[dollar_name] = deep_copy_enzo_value(value)

        return None

    if isinstance(node, ReverseDestructuring):
        # Handle reverse destructuring: source[] :> $var1, $var2

        # Check for duplicate variable names
        seen_vars = set()
        for var_name in node.target_vars:
            if var_name in seen_vars:
                raise EnzoRuntimeError(error_message_duplicate_variable_names(), code_line=node.code_line)
            seen_vars.add(var_name)

        source_value = eval_ast(node.source_expr, value_demand=True, env=env)

        # If source_value is a ReferenceWrapper, dereference it first
        if isinstance(source_value, ReferenceWrapper):
            source_value = source_value.get_value()

            # If the referenced value is a BlueprintInstantiation, evaluate it to get the list
            if isinstance(source_value, BlueprintInstantiation):
                source_value = eval_ast(source_value, value_demand=True, env=env)

        # Check if this is an EnzoList (enhanced list with key support)
        if isinstance(source_value, EnzoList):
            # Try named destructuring first (if variable names match keys)
            named_matches = 0
            for var_name in node.target_vars:
                # Check if this variable has a renamed source key
                source_key = None
                if hasattr(node, 'renamed_pairs') and node.renamed_pairs:
                    # Find the source key for this target variable
                    for src_key, target_var in node.renamed_pairs.items():
                        if target_var == var_name:
                            source_key = src_key
                            break

                # If no renamed source, use the variable name itself
                if source_key is None:
                    source_key = var_name

                # Try both with and without $ prefix for the source key
                key_candidates = [source_key]
                if source_key.startswith('$'):
                    key_candidates.append(source_key[1:])  # without $
                else:
                    key_candidates.append('$' + source_key)  # with $

                # Also try enhanced pattern matching (remove numeric suffixes)
                for key_candidate in key_candidates[:]:  # Copy list to avoid modification during iteration
                    for suffix_pattern in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        if key_candidate.endswith(suffix_pattern):
                            key_candidates.append(key_candidate[:-1])  # Remove suffix

                # Check if any key candidate exists in the list
                for key_candidate in key_candidates:
                    try:
                        source_value.get_by_key(key_candidate)
                        named_matches += 1
                        break
                    except KeyError:
                        continue

            # If most/all variables have matching keys, use named destructuring
            if named_matches >= len(node.target_vars) * 0.5:  # At least 50% match
                # Named destructuring
                for var_name in node.target_vars:
                    value = Empty()  # Default if not found

                    # Check if this variable has a renamed source key
                    source_key = None
                    if hasattr(node, 'renamed_pairs') and node.renamed_pairs:
                        # Find the source key for this target variable
                        for src_key, target_var in node.renamed_pairs.items():
                            if target_var == var_name:
                                source_key = src_key
                                break

                    # If no renamed source, use the variable name itself
                    if source_key is None:
                        source_key = var_name

                    # Try both with and without $ prefix for the source key
                    key_candidates = [source_key]
                    if source_key.startswith('$'):
                        key_candidates.append(source_key[1:])  # without $
                    else:
                        key_candidates.append('$' + source_key)  # with $

                    # Also try enhanced pattern matching (remove numeric suffixes)
                    for key_candidate in key_candidates[:]:  # Copy list to avoid modification during iteration
                        for suffix_pattern in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                            if key_candidate.endswith(suffix_pattern):
                                key_candidates.append(key_candidate[:-1])  # Remove suffix

                    # Look for the key
                    for key_candidate in key_candidates:
                        try:
                            value = source_value.get_by_key(key_candidate)
                            break
                        except KeyError:
                            continue

                    # Handle reference destructuring if specified
                    if getattr(node, 'is_reference', False):
                        # Create a reference to the source key for this variable
                        # We need to create a ListIndex node that represents source.key

                        # Extract the base variable from the source expression
                        if hasattr(node, 'source_expr') and hasattr(node.source_expr, 'target'):
                            # Handle @variable[] case - get the variable name from ReferenceAtom target
                            base_var_name = node.source_expr.target.blueprint_name
                            base_var_node = VarInvoke(base_var_name, code_line=getattr(node, 'code_line', None))
                        else:
                            # Fallback - use the source expression directly
                            base_var_node = node.source_expr

                        # Find the matching key for this variable
                        matching_key = None
                        for key_candidate in key_candidates:
                            try:
                                source_value.get_by_key(key_candidate)
                                matching_key = key_candidate
                                break
                            except KeyError:
                                continue

                        if matching_key:
                            # Remove $ prefix for property access
                            prop_name = matching_key[1:] if matching_key.startswith('$') else matching_key
                            property_access = ListIndex(
                                base=base_var_node,
                                index=TextAtom(prop_name),
                                is_property_access=True,
                                code_line=getattr(node, 'code_line', None)
                            )
                            env[var_name] = ReferenceWrapper(property_access, env)
                        else:
                            # Fallback to regular value if no key found
                            env[var_name] = deep_copy_enzo_value(value)
                    else:
                        env[var_name] = deep_copy_enzo_value(value)

                    # Also make accessible with/without $ prefix
                    if var_name.startswith('$'):
                        bare_name = var_name[1:]
                        if bare_name not in env:
                            env[bare_name] = env[var_name]
                    else:
                        dollar_name = '$' + var_name
                        if dollar_name not in env:
                            env[dollar_name] = env[var_name]

                return None

            # Fall back to positional destructuring for EnzoList
            items = source_value._elements
        elif isinstance(source_value, list):
            items = source_value
        elif isinstance(source_value, dict):
            items = list(source_value.values())
        else:
            raise EnzoRuntimeError(f"Cannot destructure non-list value: {source_value}", code_line=node.code_line)

        # Check that we have enough elements
        if len(items) < len(node.target_vars):
            raise EnzoRuntimeError(error_message_destructure_count_mismatch(), code_line=node.code_line)

        # Assign each variable
        for i, var_name in enumerate(node.target_vars):
            value = items[i] if i < len(items) else Empty()

            # Handle reference destructuring if specified
            if getattr(node, 'is_reference', False):
                # For EnzoList, try to create property reference if there's a key at this position
                if isinstance(source_value, EnzoList):
                    key_at_position = source_value.get_key_at_index(i)
                    if key_at_position:
                        # Create a property access reference
                        base_var_node = node.source_expr
                        prop_name = key_at_position[1:] if key_at_position.startswith('$') else key_at_position
                        property_access = ListIndex(
                            base=base_var_node,
                            index=TextAtom(prop_name),
                            is_property_access=True,
                            code_line=getattr(node, 'code_line', None)
                        )
                        env[var_name] = ReferenceWrapper(property_access, env)
                    else:
                        # Fallback to positional reference for positional-only elements
                        base_var_node = node.source_expr
                        index_node = NumberAtom(i)
                        list_index_ref = ListIndex(
                            base=base_var_node,
                            index=index_node,
                            code_line=getattr(node, 'code_line', None)
                        )
                        env[var_name] = ReferenceWrapper(list_index_ref, env)
                else:
                    # Create a reference to the original list element
                    base_var_node = node.source_expr
                    index_node = NumberAtom(i)
                    list_index_ref = ListIndex(
                        base=base_var_node,
                        index=index_node,
                        code_line=getattr(node, 'code_line', None)
                    )
                    env[var_name] = ReferenceWrapper(list_index_ref, env)
            else:
                env[var_name] = deep_copy_enzo_value(value)

            # Also make accessible with/without $ prefix
            if var_name.startswith('$'):
                bare_name = var_name[1:]
                if bare_name not in env:
                    env[bare_name] = env[var_name]
            else:
                dollar_name = '$' + var_name
                if dollar_name not in env:
                    env[dollar_name] = env[var_name]

        return None

    if isinstance(node, ReferenceDestructuring):
        # Handle reference destructuring: @$var1, @$var2: source[]
        source_value = eval_ast(node.source_expr, value_demand=True, env=env)

        # Ensure source is iterable
        if isinstance(source_value, EnzoList):
            items = source_value._elements
        elif isinstance(source_value, list):
            items = source_value
        elif isinstance(source_value, dict):
            items = list(source_value.values())
        else:
            raise EnzoRuntimeError(f"Cannot destructure non-list value: {source_value}", code_line=node.code_line)

        # Check that we have enough elements
        if len(items) < len(node.target_vars):
            raise EnzoRuntimeError(error_message_destructure_count_mismatch(), code_line=node.code_line)

        # Assign each variable as references
        for i, var_name in enumerate(node.target_vars):
            if i < len(items):
                # Create reference wrapper that points to the original item
                env[var_name] = ReferenceWrapper(lambda idx=i: items[idx], env)
            else:
                env[var_name] = ReferenceWrapper(lambda: Empty(), env)

            # Also make accessible with/without $ prefix
            if var_name.startswith('$'):
                bare_name = var_name[1:]
                if bare_name not in env:
                    env[bare_name] = env[var_name]
            else:
                dollar_name = '$' + var_name
                if dollar_name not in env:
                    env[dollar_name] = env[var_name]

        return None

    if isinstance(node, RestructuringBinding):
        # Handle restructuring: $var1, $var2 -> $new: source[]

        # Special case: If new_var is None, this might be reverse assignment
        # Syntax: [$var1, $var2] :> $target[] should assign values TO target
        if node.new_var is None:
            # This is reverse assignment: write target_vars values to source_expr
            target_list = eval_ast(node.source_expr, value_demand=True, env=env)

            # Create new list with current values of target_vars
            new_elements = []
            for var_name in node.target_vars:
                if var_name in env:
                    new_elements.append(env[var_name])
                else:
                    new_elements.append(Empty())

            # Replace the target list contents
            if hasattr(target_list, '_elements'):  # EnzoList
                target_list._elements.clear()
                target_list._key_map.clear()
                for i, element in enumerate(new_elements):
                    target_list._elements.append(element)
            else:
                # If it's a regular list, we need to update the variable
                # Get the target variable name
                if hasattr(node.source_expr, 'name'):
                    target_var = node.source_expr.name
                    env[target_var] = new_elements
                    # Also update without $ prefix if needed
                    if target_var.startswith('$'):
                        bare_name = target_var[1:]
                        if bare_name not in env:
                            env[bare_name] = new_elements
                    else:
                        dollar_name = '$' + target_var
                        if dollar_name not in env:
                            env[dollar_name] = new_elements

            return None

        # Regular restructuring logic (extraction)
        # Check for duplicate variable names
        seen_vars = set()
        for var_name in node.target_vars:
            if var_name in seen_vars:
                raise EnzoRuntimeError(error_message_duplicate_variable_names(), code_line=node.code_line)
            seen_vars.add(var_name)

        source_value = eval_ast(node.source_expr, value_demand=True, env=env)

        # If source_value is a ReferenceWrapper, dereference it first
        if isinstance(source_value, ReferenceWrapper):
            source_value = source_value.get_value()

            # If the referenced value is a BlueprintInstantiation, evaluate it to get the list
            if isinstance(source_value, BlueprintInstantiation):
                source_value = eval_ast(source_value, value_demand=True, env=env)

        # Check if this is an EnzoList (enhanced list with key support)
        if isinstance(source_value, EnzoList):
            # Try named destructuring first (if variable names match keys)
            named_matches = 0
            for var_name in node.target_vars:
                # Try both with and without $ prefix
                key_candidates = [var_name]
                if var_name.startswith('$'):
                    key_candidates.append(var_name[1:])  # without $
                else:
                    key_candidates.append('$' + var_name)  # with $

                # Also try enhanced pattern matching (remove numeric suffixes)
                for key_candidate in key_candidates[:]:  # Copy list to avoid modification during iteration
                    for suffix_pattern in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        if key_candidate.endswith(suffix_pattern):
                            key_candidates.append(key_candidate[:-1])  # Remove suffix

                # Try to find a matching key
                value = None
                for key_candidate in key_candidates:
                    try:
                        value = source_value.get_by_key(key_candidate)
                        named_matches += 1
                        break
                    except KeyError:
                        continue

                if value is not None:
                    env[var_name] = deep_copy_enzo_value(value)
                    # Also make accessible with/without $ prefix
                    if var_name.startswith('$'):
                        bare_name = var_name[1:]
                        if bare_name not in env:
                            env[bare_name] = deep_copy_enzo_value(value)
                    else:
                        dollar_name = '$' + var_name
                        if dollar_name not in env:
                            env[dollar_name] = deep_copy_enzo_value(value)

            # Use named destructuring if we got matches for more than 50% of variables
            if named_matches >= len(node.target_vars) * 0.5:
                # Now set the renamed variable to the last extracted value
                if node.target_vars:  # Make sure we have variables
                    last_var = node.target_vars[-1]
                    if last_var in env:
                        env[node.new_var] = env[last_var]
                        # Also make accessible with/without $ prefix
                        if node.new_var.startswith('$'):
                            bare_name = node.new_var[1:]
                            if bare_name not in env:
                                env[bare_name] = env[last_var]
                        else:
                            dollar_name = '$' + node.new_var
                            if dollar_name not in env:
                                env[dollar_name] = env[last_var]
                return None

            # Fall back to positional destructuring for EnzoList
            items = source_value._elements
        elif isinstance(source_value, list):
            items = source_value
        elif isinstance(source_value, dict):
            items = list(source_value.values())
        else:
            raise EnzoRuntimeError(f"Cannot destructure non-list value: {source_value}", code_line=node.code_line)

        # Check that we have enough elements
        if len(items) < len(node.target_vars):
            raise EnzoRuntimeError(error_message_destructure_count_mismatch(), code_line=node.code_line)

        # First, assign the original variables
        for i, var_name in enumerate(node.target_vars):
            value = items[i] if i < len(items) else Empty()

            if getattr(node, 'is_reference', False):
                env[var_name] = ReferenceWrapper(lambda idx=i: items[idx], env)
            else:
                env[var_name] = deep_copy_enzo_value(value)

            # Also make accessible with/without $ prefix
            if var_name.startswith('$'):
                bare_name = var_name[1:]
                if bare_name not in env:
                    env[bare_name] = env[var_name]
            else:
                dollar_name = '$' + var_name
                if dollar_name not in env:
                    env[dollar_name] = env[var_name]

        # Then assign the new composite variable containing the extracted values
        extracted_values = [items[i] if i < len(items) else Empty() for i in range(len(node.target_vars))]
        new_list = EnzoList()
        for val in extracted_values:
            new_list.append(val)

        if node.new_var is not None:
            env[node.new_var] = new_list

            # Also make accessible with/without $ prefix
            if node.new_var.startswith('$'):
                bare_name = node.new_var[1:]
                if bare_name not in env:
                    env[bare_name] = new_list
            else:
                dollar_name = '$' + node.new_var
                if dollar_name not in env:
                    env[dollar_name] = new_list

        return None

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
                    return invoke_function(referenced_val, [], env, self_obj=None, is_loop_context=is_loop_context)
            return referenced_val

        # Handle list element reference: return the current value of the list element
        if isinstance(val, ListElementReference):
            referenced_val = val.get_value()
            # Check if the referenced value is a function
            if isinstance(referenced_val, EnzoFunction):
                # Auto-invoke functions when referenced with $ sigil in value_demand context
                if value_demand:
                    if not name.startswith('$'):
                        raise EnzoRuntimeError("error: expected function reference (@) or function invocation ($)", code_line=node.code_line)
                    return invoke_function(referenced_val, [], env, self_obj=None, is_loop_context=is_loop_context)
            return referenced_val

        # Check if this is a function
        if isinstance(val, EnzoFunction):
            # Auto-invoke functions when referenced with $ sigil in value_demand context
            if value_demand:
                # Bare function names (without $ sigil) cannot be auto-invoked
                if not name.startswith('$'):
                    raise EnzoRuntimeError("error: expected function reference (@) or function invocation ($)", code_line=node.code_line)
                return invoke_function(val, [], env, self_obj=None, is_loop_context=is_loop_context)
        return val
    if isinstance(node, FunctionRef):
        # Evaluate the expression to get the function object
        val = eval_ast(node.expr, value_demand=False, env=env)
        if not isinstance(val, EnzoFunction):
            raise EnzoTypeError(error_message_not_a_function(val), code_line=node.code_line)
        return val
    if isinstance(node, ReferenceAtom):
        target = node.target

        # Special handling for BlueprintInstantiation references (e.g., @person8[])
        if isinstance(target, BlueprintInstantiation):
            # Check if this is actually a reference to an existing variable, not a blueprint
            var_name = target.blueprint_name
            if var_name in env and not isinstance(env[var_name], BlueprintAtom):
                # This is a reference to an existing variable, not a blueprint instantiation
                # Create a VarInvoke node instead and wrap it as a reference
                var_invoke = VarInvoke(var_name, code_line=getattr(target, 'code_line', None))
                return ReferenceWrapper(var_invoke, env)

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
            return invoke_function(fn, [], env, self_obj=None, is_loop_context=is_loop_context)
        else:
            return EnzoFunction(node.params, node.local_vars, node.body, env, getattr(node, 'is_multiline', False))
    if isinstance(node, AddNode):
        left = eval_ast(node.left, value_demand=True, env=env, is_loop_context=is_loop_context)
        right = eval_ast(node.right, value_demand=True, env=env, is_loop_context=is_loop_context)
        return left + right
    if isinstance(node, SubNode):
        left = eval_ast(node.left, value_demand=True, env=env, is_loop_context=is_loop_context)
        right = eval_ast(node.right, value_demand=True, env=env, is_loop_context=is_loop_context)
        return left - right
    if isinstance(node, MulNode):
        left = eval_ast(node.left, value_demand=True, env=env, is_loop_context=is_loop_context)
        right = eval_ast(node.right, value_demand=True, env=env, is_loop_context=is_loop_context)
        return left * right
    if isinstance(node, DivNode):
        left = eval_ast(node.left, value_demand=True, env=env, is_loop_context=is_loop_context)
        right = eval_ast(node.right, value_demand=True, env=env, is_loop_context=is_loop_context)
        return left / right
    if isinstance(node, ModNode):
        left = eval_ast(node.left, value_demand=True, env=env, is_loop_context=is_loop_context)
        right = eval_ast(node.right, value_demand=True, env=env, is_loop_context=is_loop_context)

        # Check for modulo by zero
        if right == 0:
            raise EnzoRuntimeError("error: No division by zero", code_line=getattr(node, 'code_line', None))

        # Implement Euclidean modulo: result is always non-negative
        # For Euclidean modulo: a = bq + r where 0 ≤ r < |b|
        result = left % right
        if result < 0:
            result += abs(right)
        return result
    if isinstance(node, Invoke):
        left = eval_ast(node.func, value_demand=False, env=env, is_loop_context=is_loop_context)  # Get function object, don't invoke it yet

        # If left is a ReferenceWrapper that refers to a function, dereference it
        if isinstance(left, ReferenceWrapper):
            left = left.get_value()

        # Evaluate arguments, but preserve ReferenceWrapper objects for function calls
        args = []
        for arg in node.args:
            arg_result = eval_ast(arg, value_demand=False, env=env, is_loop_context=is_loop_context)  # Don't dereference yet
            if isinstance(arg_result, ReferenceWrapper):
                # Keep the ReferenceWrapper for the function call
                args.append(arg_result)
            else:
                # For non-references, evaluate normally
                args.append(eval_ast(arg, value_demand=True, env=env, is_loop_context=is_loop_context))

        # EnzoList indexing and keyed access
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
                # String values should be treated as invalid index types, not property access
                elif isinstance(key, str):
                    raise EnzoTypeError(error_message_index_must_be_integer(), code_line=getattr(node, 'code_line', None))
                else:
                    raise EnzoTypeError(error_message_index_must_be_integer(), code_line=getattr(node, 'code_line', None))
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
            return invoke_function(left, args, env, self_obj=self_obj, is_loop_context=is_loop_context)
        # Not a list or function
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
            return invoke_function(fn, [], pipeline_env, self_obj=None, is_loop_context=is_loop_context)
        # For expressions that can potentially reference $this, evaluate in pipeline environment
        elif isinstance(right_expr, (AddNode, SubNode, MulNode, DivNode, ModNode, VarInvoke, Invoke, TextAtom, ListIndex, ReferenceAtom, IfStatement)):
            return eval_ast(right_expr, value_demand=True, env=pipeline_env)
        else:
            # For literals and other nodes that can't reference $this, this doesn't make sense
            raise EnzoRuntimeError("error: pipeline expects function atom after `then`", code_line=getattr(node, 'code_line', None))
    if isinstance(node, BindOrRebind):
        target = node.target
        value = eval_ast(node.value, value_demand=True, env=env, outer_env=outer_env, loop_locals=loop_locals)

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
            if isinstance(val, ListElementReference):
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
            # For rebinding operations:
            # - If variable was shadowed in this loop (in loop_locals), rebind in current env
            # - If variable exists in outer_env and not shadowed, rebind in outer_env
            # - Otherwise rebind in current env
            if loop_locals is not None and name in loop_locals:
                # Variable was shadowed in this loop - rebind in current env only
                target_env = env
                update_current_env = False
            elif outer_env is not None and name in outer_env:
                # Variable exists in outer scope and not shadowed - rebind there
                target_env = outer_env
                # Also update current env to maintain consistency
                update_current_env = True
            else:
                # Variable doesn't exist in outer scope, or no outer scope - use current
                target_env = env
                update_current_env = False

            if name not in target_env:
                target_env[name] = actual_value
                if update_current_env and env is not target_env:
                    env[name] = actual_value
                return None
            old_val = target_env[name]
            if not isinstance(old_val, Empty) and enzo_type(old_val) != enzo_type(actual_value):
                raise EnzoRuntimeError(error_message_cannot_bind(enzo_type(actual_value), enzo_type(old_val)), code_line=node.code_line)
            target_env[name] = actual_value
            # Also update current env to maintain consistency for reads
            if update_current_env and env is not target_env:
                env[name] = actual_value
            return None
        # Assignment to variable via VarInvoke
        if isinstance(target, VarInvoke):
            name = target.name
            t_code_line = getattr(target, 'code_line', node.code_line)
            # For rebinding operations: same logic as string targets
            if loop_locals is not None and name in loop_locals:
                # Variable was shadowed in this loop - rebind in current env only
                target_env = env
                update_current_env = False
            elif outer_env is not None and name in outer_env:
                # Variable exists in outer scope and not shadowed - rebind there
                target_env = outer_env
                # Also update current env to maintain consistency
                update_current_env = True
            else:
                # Variable doesn't exist in outer scope, or no outer scope - use current
                target_env = env
                update_current_env = False

            if name not in target_env:
                target_env[name] = actual_value
                if update_current_env and env is not target_env:
                    env[name] = actual_value
                return None
            old_val = target_env[name]            # Special case: if the target variable contains a ReferenceWrapper,
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
                    # Complex reference (e.g., to list index) - implement assignment
                    if isinstance(ref_expr, ListIndex):
                        # Handle assignment to referenced list property
                        base_result = eval_ast(ref_expr.base, env=ref_env, value_demand=False)

                        # If the base is a ReferenceWrapper, we need to operate on the referenced object
                        if isinstance(base_result, ReferenceWrapper):
                            base = base_result.get_value()
                        else:
                            base = base_result

                        idx = eval_ast(ref_expr.index, env=ref_env)

                        # Handle EnzoList property assignment
                        if isinstance(base, EnzoList):
                            if isinstance(idx, str) and getattr(ref_expr, 'is_property_access', False):
                                # Property assignment (e.g., $list.name := value)
                                try:
                                    base.set_by_key(f'${idx}', actual_value)
                                    return None
                                except KeyError:
                                    raise EnzoRuntimeError(error_message_list_property_not_found(idx), code_line=t_code_line)
                            else:
                                raise EnzoTypeError(error_message_cant_use_text_as_index(), code_line=t_code_line)
                        else:
                            raise EnzoTypeError(error_message_index_applies_to_lists(), code_line=t_code_line)
                    else:
                        raise EnzoRuntimeError("Cannot assign to complex reference", code_line=t_code_line)

            elif isinstance(old_val, ListElementReference):
                # Special case: if the target variable contains a ListElementReference,
                # we need to update the original list element
                list_old_val = old_val.get_value()
                if not isinstance(list_old_val, Empty) and enzo_type(list_old_val) != enzo_type(actual_value):
                    raise EnzoRuntimeError(error_message_cannot_bind(enzo_type(actual_value), enzo_type(list_old_val)), code_line=node.code_line)
                old_val.set_value(actual_value)
                return None

            # Normal variable assignment
            if not isinstance(old_val, Empty) and enzo_type(old_val) != enzo_type(actual_value):
                raise EnzoRuntimeError(error_message_cannot_bind(enzo_type(actual_value), enzo_type(old_val)), code_line=t_code_line)
            target_env[name] = actual_value
            # Also update current env to maintain consistency for reads
            if update_current_env and env is not target_env:
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

        # Handle assignment to BlueprintInstantiation with empty field_values (list assignment)
        if isinstance(target, BlueprintInstantiation) and not target.field_values:
            # This is $variable[] <: value - assign value to the variable
            var_name = target.blueprint_name
            if var_name not in env:
                raise EnzoRuntimeError(error_message_unknown_variable(var_name), code_line=getattr(node, 'code_line', None))

            original_var = env[var_name]

            # If the original variable is an EnzoList, we want to preserve its structure
            # and update it intelligently rather than replacing it entirely
            if isinstance(original_var, EnzoList) and isinstance(value, (list, EnzoList)):
                # Smart update: try to match up values with existing keys
                if isinstance(value, EnzoList):
                    # If the new EnzoList has keys, copy them
                    if value._key_map:
                        for key in value._key_map:
                            original_var.set_key(key, value.get_by_key(key))
                    else:
                        # If the new EnzoList only has positional elements, map them to existing keys
                        existing_keys = list(original_var._key_map.keys())
                        for i, val in enumerate(value._elements):
                            if i < len(existing_keys):
                                key = existing_keys[i]
                                original_var.set_key(key, val)
                elif isinstance(value, list):
                    # If it's a regular list, try to map values to existing keys
                    existing_keys = list(original_var._key_map.keys())
                    for i, val in enumerate(value):
                        if i < len(existing_keys):
                            # Update existing key with new value
                            key = existing_keys[i]
                            original_var.set_key(key, val)
                # Don't need to reassign - we modified the existing object
            else:
                # Replace the entire variable with the new value (fallback)
                env[var_name] = deep_copy_enzo_value(value)

                # Also update with/without $ prefix
                if var_name.startswith('$'):
                    bare_name = var_name[1:]
                    if bare_name in env:
                        env[bare_name] = deep_copy_enzo_value(value)
                else:
                    dollar_name = '$' + var_name
                    if dollar_name in env:
                        env[dollar_name] = deep_copy_enzo_value(value)
            return None

        raise EnzoRuntimeError(error_message_cannot_bind_target(target), code_line=getattr(node, 'code_line', None))
    if isinstance(node, ListIndex):
        base = eval_ast(node.base, env=env)
        idx = eval_ast(node.index, env=env)
        t_code_line = getattr(node, 'code_line', code_line)

        # Handle EnzoList indexing
        if isinstance(base, EnzoList):
            try:
                if isinstance(idx, (int, float)):
                    if isinstance(idx, float) and not idx.is_integer():
                        raise EnzoTypeError(error_message_index_must_be_integer(), code_line=t_code_line)
                    val = base.get_by_index(int(idx))
                    # Auto-invoke functions in value demand context
                    if value_demand and isinstance(val, EnzoFunction):
                        return invoke_function(val, [], env, self_obj=None, is_loop_context=is_loop_context)
                    return val
                elif isinstance(idx, str):
                    # Check if this is property access (.foo) or string indexing (."foo")
                    if getattr(node, 'is_property_access', False):
                        # Property access (e.g., $list.name)
                        val = base.get_by_key(idx)
                        # Auto-invoke functions in value demand context
                        if value_demand and isinstance(val, EnzoFunction):
                            return invoke_function(val, [], env, self_obj=base, is_loop_context=is_loop_context)
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

        # Check if this is variant access before falling back to error handling
        if isinstance(idx, str) and getattr(node, 'is_property_access', False):
            # Check if base is a variant group (has a variants attribute)
            if hasattr(base, 'variants'):
                # This is variant access: VariantGroup.VariantName
                variant_group_name = None
                if isinstance(node.base, VarInvoke):
                    variant_group_name = node.base.name

                # Check if it's a valid variant
                if idx not in base.variants:
                    raise EnzoRuntimeError(f"error: '{idx}' not a valid {variant_group_name}", code_line=t_code_line)

                # Create a variant instance using the global class
                return EnzoVariantInstance(variant_group_name, idx)
            else:
                # Property access on non-list objects should give "list property not found"
                raise EnzoRuntimeError(error_message_list_property_not_found(idx), code_line=t_code_line)

        # Legacy list handling and property access on non-EnzoList objects
        if isinstance(idx, str):
            # String indexing should give "list index must be an integer"
            raise EnzoRuntimeError(error_message_index_must_be_integer(), code_line=t_code_line)
        if not isinstance(base, list):
            if isinstance(node.base, VarInvoke):
                raise EnzoRuntimeError(error_message_index_applies_to_lists(), code_line=t_code_line)
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        if not isinstance(idx, int) or idx < 1 or idx > len(base):
            raise EnzoRuntimeError(error_message_list_index_out_of_range(), code_line=t_code_line)
        val = base[idx - 1]
        # Auto-invoke functions in value demand context
        if value_demand and isinstance(val, EnzoFunction):
            return invoke_function(val, [], env, self_obj=None, is_loop_context=is_loop_context)
        return val
    if isinstance(node, ParameterDeclaration):
        raise EnzoRuntimeError(error_message_param_outside_function(), code_line=getattr(node, 'code_line', None))

    # Blueprint evaluation
    if isinstance(node, BlueprintAtom):
        # BlueprintAtom represents a blueprint definition
        # For now, we'll store it as-is in the environment when it's bound to a name
        return node

    if isinstance(node, BlueprintInstantiation):
        # BlueprintInstantiation represents creating an instance from a blueprint
        blueprint_name = node.blueprint_name

        # Look up the blueprint definition
        if blueprint_name not in env:
            raise EnzoRuntimeError(f"error: unknown blueprint '{blueprint_name}'", code_line=getattr(node, 'code_line', None))

        blueprint_def = env[blueprint_name]
        if not isinstance(blueprint_def, BlueprintAtom):
            raise EnzoRuntimeError(f"error: '{blueprint_name}' is not a blueprint", code_line=getattr(node, 'code_line', None))

        # Create an instance by evaluating the field values and creating an EnzoList
        instance = EnzoList(is_blueprint_instance=True)

        # Create a map of provided field values for efficient lookup
        provided_values = {}
        for field_name, field_value in node.field_values:
            clean_field_name = field_name[1:] if field_name.startswith('$') else field_name
            provided_values[clean_field_name] = field_value

        # Iterate through blueprint fields in their definition order
        for field_name, field_default in blueprint_def.fields:
            clean_field_name = field_name[1:] if field_name.startswith('$') else field_name
            key_with_prefix = f'${clean_field_name}'

            if clean_field_name in provided_values:
                # Use the provided value
                evaluated_value = eval_ast(provided_values[clean_field_name], value_demand=True, env=env)
                instance.set_key(key_with_prefix, evaluated_value)
            elif field_default is not None:
                # Use the default value - preserve function objects, don't auto-invoke
                if isinstance(field_default, FunctionAtom):
                    default_value = eval_ast(field_default, value_demand=False, env=env)
                else:
                    default_value = eval_ast(field_default, value_demand=True, env=env)
                instance.set_key(key_with_prefix, default_value)

        # TODO: Add type validation

        return instance

    if isinstance(node, BlueprintComposition):
        # BlueprintComposition represents composing multiple blueprints
        combined_fields = []
        seen_field_names = set()

        for blueprint_item in node.blueprints:
            blueprint_def = None

            if isinstance(blueprint_item, str):
                # Blueprint name - look it up in environment
                if blueprint_item not in env:
                    raise EnzoRuntimeError(f"error: unknown blueprint '{blueprint_item}'", code_line=getattr(node, 'code_line', None))
                blueprint_def = env[blueprint_item]
                if not isinstance(blueprint_def, BlueprintAtom):
                    raise EnzoRuntimeError(f"error: '{blueprint_item}' is not a blueprint", code_line=getattr(node, 'code_line', None))
            elif isinstance(blueprint_item, BlueprintAtom):
                # Inline blueprint definition
                blueprint_def = blueprint_item
            else:
                raise EnzoRuntimeError(f"error: invalid blueprint component in composition", code_line=getattr(node, 'code_line', None))

            # Check for field conflicts and collect fields
            for field_name, field_default in blueprint_def.fields:
                clean_field_name = field_name[1:] if field_name.startswith('$') else field_name
                if clean_field_name in seen_field_names:
                    raise EnzoRuntimeError(f"error: duplicate property '{clean_field_name}' in composed blueprints", code_line=getattr(node, 'code_line', None))
                seen_field_names.add(clean_field_name)
                combined_fields.append((field_name, field_default))

        # Return a new blueprint with the combined fields
        return BlueprintAtom(combined_fields, code_line=getattr(node, 'code_line', None))

    if isinstance(node, VariantGroup):
        # VariantGroup represents a variant group definition
        # Process variants and register inline blueprint definitions
        variant_names = []
        group_blueprint = None  # Store the blueprint if the group name matches a variant

        for variant in node.variants:
            if isinstance(variant, tuple):
                # Inline blueprint definition: (variant_name, blueprint_def)
                variant_name, blueprint_def = variant
                variant_names.append(variant_name)

                if variant_name == node.name:
                    # This variant has the same name as the group - store separately
                    group_blueprint = blueprint_def
                    env[f"__{node.name}__blueprint"] = blueprint_def
                else:
                    # Register other blueprints normally
                    env[variant_name] = blueprint_def
            else:
                # Simple variant name - assume it's already defined elsewhere
                variant_names.append(variant)

        # Create a runtime variant group that validates variant access
        return EnzoVariantGroup(node.name, variant_names, group_blueprint)

    if isinstance(node, VariantGroupExtension):
        # VariantGroupExtension represents extending an existing variant group
        group_name = node.name

        # Check if the variant group exists
        if group_name not in env:
            raise EnzoRuntimeError(f"error: cannot extend undefined variant group '{group_name}'", code_line=getattr(node, 'code_line', None))

        existing_group = env[group_name]
        if not isinstance(existing_group, EnzoVariantGroup):
            raise EnzoRuntimeError(f"error: '{group_name}' is not a variant group", code_line=getattr(node, 'code_line', None))

        # Process new variants to add
        new_variant_names = []
        for variant in node.variants:
            if isinstance(variant, tuple):
                # Inline blueprint definition: (variant_name, blueprint_def)
                variant_name, blueprint_def = variant
                new_variant_names.append(variant_name)
                env[variant_name] = blueprint_def
            else:
                # Simple variant name
                new_variant_names.append(variant)

        # Create extended variant group by merging with existing
        all_variants = list(existing_group.variants) + new_variant_names
        extended_group = EnzoVariantGroup(group_name, all_variants, existing_group.group_blueprint)

        # Update the environment with the extended group
        env[group_name] = extended_group

        # Return None for extensions - they are side-effect operations
        return None

    if isinstance(node, VariantAccess):
        # VariantAccess represents accessing a variant (e.g., Magic-Type.Fire)
        variant_group_name = node.variant_group_name
        variant_name = node.variant_name

        # Look up the variant group
        if variant_group_name not in env:
            raise EnzoRuntimeError(f"error: unknown variant group '{variant_group_name}'", code_line=getattr(node, 'code_line', None))

        variant_group = env[variant_group_name]

        # Check if it's a valid variant
        if hasattr(variant_group, 'variants') and variant_name not in variant_group.variants:
            raise EnzoRuntimeError(f"error: '{variant_name}' not a valid {variant_group_name}", code_line=getattr(node, 'code_line', None))

        # Create a variant instance using the global class
        return EnzoVariantInstance(variant_group_name, variant_name)
    if isinstance(node, VariantInstantiation):
        # VariantInstantiation represents creating an instance of a specific variant
        variant_group_name = node.variant_group_name
        variant_name = node.variant_name

        # Look up the variant group to validate the variant
        if variant_group_name not in env:
            raise EnzoRuntimeError(f"error: unknown variant group '{variant_group_name}'", code_line=getattr(node, 'code_line', None))

        variant_group = env[variant_group_name]
        if not hasattr(variant_group, 'variants') or variant_name not in variant_group.variants:
            raise EnzoRuntimeError(f"error: '{variant_name}' not a valid {variant_group_name}", code_line=getattr(node, 'code_line', None))

        # Collect blueprints to compose for this variant
        blueprints_to_compose = []

        # Check if there's a preserved group blueprint (for cases like Monster3.Monster3)
        group_blueprint_key = f"__{variant_group_name}__blueprint"
        if group_blueprint_key in env:
            blueprints_to_compose.append(env[group_blueprint_key])

        # Look up the specific variant blueprint
        if variant_name not in env:
            raise EnzoRuntimeError(f"error: unknown variant '{variant_name}'", code_line=getattr(node, 'code_line', None))

        variant_blueprint = env[variant_name]
        if not isinstance(variant_blueprint, BlueprintAtom):
            raise EnzoRuntimeError(f"error: '{variant_name}' is not a blueprint", code_line=getattr(node, 'code_line', None))

        # Add the variant blueprint (avoid duplicates)
        if not blueprints_to_compose or variant_blueprint != blueprints_to_compose[0]:
            blueprints_to_compose.append(variant_blueprint)

        # Create an instance by combining all blueprints
        instance = EnzoList(is_blueprint_instance=True)

        # Create a map of provided field values for efficient lookup
        provided_values = {}
        for field_name, field_value in node.field_values:
            clean_field_name = field_name[1:] if field_name.startswith('$') else field_name
            provided_values[clean_field_name] = field_value

        # Collect all fields from all blueprints (later blueprints override earlier ones)
        all_fields = []
        seen_field_names = set()

        for blueprint in blueprints_to_compose:
            for field_name, field_default in blueprint.fields:
                clean_field_name = field_name[1:] if field_name.startswith('$') else field_name
                if clean_field_name not in seen_field_names:
                    all_fields.append((field_name, field_default))
                    seen_field_names.add(clean_field_name)
                else:
                    # Override: remove the previous field and add the new one
                    all_fields = [(fn, fd) for fn, fd in all_fields if (fn[1:] if fn.startswith('$') else fn) != clean_field_name]
                    all_fields.append((field_name, field_default))

        # Iterate through all combined fields in their definition order
        for field_name, field_default in all_fields:
            clean_field_name = field_name[1:] if field_name.startswith('$') else field_name
            key_with_prefix = f'${clean_field_name}'

            if clean_field_name in provided_values:
                # Use the provided value
                evaluated_value = eval_ast(provided_values[clean_field_name], value_demand=True, env=env)
                instance.set_key(key_with_prefix, evaluated_value)
            elif field_default is not None:
                # Use the default value - preserve function objects, don't auto-invoke
                if isinstance(field_default, FunctionAtom):
                    default_value = eval_ast(field_default, value_demand=False, env=env)
                else:
                    default_value = eval_ast(field_default, value_demand=True, env=env)
                instance.set_key(key_with_prefix, default_value)

        return instance

    # Control flow evaluation
    if isinstance(node, IfStatement):
        # Check if this is a non-exclusive multi-branch
        if hasattr(node, 'is_non_exclusive_multi_branch') and node.is_non_exclusive_multi_branch:
            # For non-exclusive multi-branch, evaluate all conditions and execute all matching ones
            results = []
            any_executed = False

            try:
                for condition, then_block in node.all_branches:
                    condition_result = eval_ast(condition, env=env, is_loop_context=is_loop_context)
                    if _is_truthy(condition_result):
                        any_executed = True
                        # Execute this branch and collect all results
                    for stmt in then_block:
                        result = eval_ast(stmt, env=env, is_loop_context=is_loop_context, is_function_context=is_function_context, outer_env=outer_env, loop_locals=loop_locals)
                        if result is not None:
                            results.append(result)                # If no branches executed and there's an else block, execute it
                if not any_executed and node.else_block:
                    for stmt in node.else_block:
                        result = eval_ast(stmt, env=env, is_loop_context=is_loop_context, is_function_context=is_function_context, outer_env=outer_env, loop_locals=loop_locals)
                        if result is not None:
                            results.append(result)
            except (EndLoopSignal, RestartLoopSignal) as signal:
                # Collect any results that were accumulated before the signal, then re-raise
                if results and hasattr(signal, 'last_result'):
                    # If signal doesn't have a result yet, store our collected results
                    if signal.last_result is None:
                        signal.last_result = results[-1] if len(results) == 1 else results if results else None
                elif results and not hasattr(signal, 'last_result'):
                    # Add last_result attribute with our collected results
                    signal.last_result = results[-1] if len(results) == 1 else results if results else None
                raise

            # Return all results as a list if there are multiple, or the single result
            if len(results) == 0:
                return None
            elif len(results) == 1:
                return results[0]
            else:
                return results
        else:
            # Regular exclusive if statement
            condition_result = eval_ast(node.condition, env=env, is_loop_context=is_loop_context)
            if _is_truthy(condition_result):
                # Execute then block - collect all non-None results
                results = []
                try:
                    for stmt in node.then_block:
                        result = eval_ast(stmt, env=env, is_loop_context=is_loop_context, is_function_context=is_function_context, outer_env=outer_env, loop_locals=loop_locals)
                        if result is not None:
                            results.append(result)
                except (EndLoopSignal, RestartLoopSignal) as signal:
                    # Collect any results that were accumulated before the signal, then re-raise
                    if results and hasattr(signal, 'last_result'):
                        # If signal doesn't have a result yet, store our collected results
                        if signal.last_result is None:
                            signal.last_result = results[-1] if len(results) == 1 else results if results else None
                    elif results and not hasattr(signal, 'last_result'):
                        # Add last_result attribute with our collected results
                        signal.last_result = results[-1] if len(results) == 1 else results if results else None
                    raise

                # Return all results as a list if there are multiple, or the single result
                if len(results) == 0:
                    return None
                elif len(results) == 1:
                    return results[0]
                else:
                    return results
            elif node.else_block:
                # Execute else block - collect all non-None results
                results = []
                try:
                    for stmt in node.else_block:
                        result = eval_ast(stmt, env=env, is_loop_context=is_loop_context, is_function_context=is_function_context, outer_env=outer_env, loop_locals=loop_locals)
                        if result is not None:
                            results.append(result)
                except (EndLoopSignal, RestartLoopSignal):
                    # Re-raise loop control signals so they propagate to the loop
                    raise

                # Return all results as a list if there are multiple, or the single result
                if len(results) == 0:
                    return None
                elif len(results) == 1:
                    return results[0]
                else:
                    return results
            return None

    if isinstance(node, LoopStatement):
        # Handle different loop types
        if node.loop_type == "basic":
            # Basic infinite loop - only exits with end-loop
            results = []
            max_iterations = 10000  # Safety limit
            iteration_count = 0

            # Create a loop environment that allows shadowing but preserves outer scope
            # Start with a copy of the outer environment
            loop_env = env.copy()
            # Track which variables were created in loop scope for shadowing behavior
            loop_locals = set()

            while iteration_count < max_iterations:
                try:
                    # Execute loop body in the loop environment
                    # Use is_function_context=True to allow variable shadowing
                    # Pass outer_env so that rebinding operations can affect outer scope
                    # Pass loop_locals to track which variables are shadowed
                    # Pass is_loop_context=True so end-loop/restart-loop work
                    for stmt in node.body:
                        result = eval_ast(stmt, env=loop_env, is_function_context=True, outer_env=env, loop_locals=loop_locals, is_loop_context=True)
                        if result is not None:
                            results.append(result)
                except EndLoopSignal:
                    break
                except RestartLoopSignal:
                    # Skip to next iteration without executing remaining body statements
                    iteration_count += 1
                    continue
                iteration_count += 1

            if iteration_count >= max_iterations:
                raise EnzoRuntimeError("Loop exceeded maximum iterations (possible infinite loop)", code_line=node.code_line)
            return results

        elif node.loop_type == "while":
            # While loop - continues while condition is true
            results = []
            max_iterations = 10000  # Safety limit
            iteration_count = 0

            while iteration_count < max_iterations:
                # Evaluate condition
                condition_result = eval_ast(node.condition, env=env, is_loop_context=is_loop_context)
                if not _is_truthy(condition_result):
                    break

                try:
                    # Create a fresh environment for each iteration to allow shadowing
                    loop_env = env.copy()
                    loop_locals = set()  # Track variables created in this iteration
                    # Execute loop body
                    for stmt in node.body:
                        result = eval_ast(stmt, env=loop_env, is_function_context=True, outer_env=env, loop_locals=loop_locals, is_loop_context=True)
                        if result is not None:
                            results.append(result)
                except EndLoopSignal as signal:
                    # Collect any result that was produced before end-loop
                    if hasattr(signal, 'last_result') and signal.last_result is not None:
                        results.append(signal.last_result)
                    break
                except RestartLoopSignal as signal:
                    # Collect any result that was produced before restart-loop
                    if hasattr(signal, 'last_result') and signal.last_result is not None:
                        results.append(signal.last_result)
                    # Skip to next iteration without executing remaining body statements
                    pass
                iteration_count += 1

            if iteration_count >= max_iterations:
                raise EnzoRuntimeError("While loop exceeded maximum iterations (possible infinite loop)", code_line=node.code_line)
            return results

        elif node.loop_type == "until":
            # Until loop - continues until condition becomes true
            results = []
            max_iterations = 10000  # Safety limit
            iteration_count = 0

            while iteration_count < max_iterations:
                # Evaluate condition (opposite of while)
                condition_result = eval_ast(node.condition, env=env, is_loop_context=is_loop_context)
                if _is_truthy(condition_result):
                    break

                try:
                    # Create a fresh environment for each iteration to allow shadowing
                    loop_env = env.copy()
                    loop_locals = set()  # Track variables created in this iteration
                    # Execute loop body
                    for stmt in node.body:
                        result = eval_ast(stmt, env=loop_env, is_function_context=True, outer_env=env, loop_locals=loop_locals, is_loop_context=True)
                        if result is not None:
                            results.append(result)
                except EndLoopSignal as signal:
                    # Collect any result that was produced before end-loop
                    if hasattr(signal, 'last_result') and signal.last_result is not None:
                        results.append(signal.last_result)
                    break
                except RestartLoopSignal as signal:
                    # Collect any result that was produced before restart-loop
                    if hasattr(signal, 'last_result') and signal.last_result is not None:
                        results.append(signal.last_result)
                    # Skip to next iteration without executing remaining body statements
                    pass
                iteration_count += 1

            if iteration_count >= max_iterations:
                raise EnzoRuntimeError("Until loop exceeded maximum iterations (possible infinite loop)", code_line=node.code_line)
            return results

        elif node.loop_type == "for":
            # For loop - iterate over a list
            # Evaluate the iterable
            iterable_value = eval_ast(node.iterable, env=env, is_loop_context=is_loop_context)

            # Ensure it's iterable
            if not isinstance(iterable_value, (list, EnzoList)):
                raise EnzoRuntimeError(error_message_for_loop_non_iterable(), code_line=node.code_line)

            results = []

            # For live iteration, we always iterate over the original list
            # This allows modifications during iteration to be immediately visible
            iteration_list = iterable_value

            # Create a new scope for the loop variable
            loop_env = env.copy()

            i = 0
            while i < len(iteration_list):
                try:
                    # Create a fresh loop_locals set for each iteration
                    loop_locals = set()
                    item = iteration_list[i]
                    
                    if node.is_reference:
                        # Reference semantics - bind to a reference of the original list element
                        # Store with $ prefix for proper variable access
                        var_name = f"${node.variable}" if not node.variable.startswith('$') else node.variable
                        loop_env[var_name] = ListElementReference(iterable_value, i)
                    else:
                        # Copy semantics - bind to a copy of the item
                        var_name = f"${node.variable}" if not node.variable.startswith('$') else node.variable
                        loop_env[var_name] = deep_copy_enzo_value(item) if hasattr(item, '__dict__') else item

                    # Execute the loop body
                    for stmt in node.body:
                        result = eval_ast(stmt, env=loop_env, is_loop_context=True, is_function_context=True, outer_env=env, loop_locals=loop_locals)
                        if result is not None:
                            results.append(result)

                    # Move to next iteration
                    i += 1

                except EndLoopSignal as signal:
                    # Collect any result that was produced before end-loop
                    if hasattr(signal, 'last_result') and signal.last_result is not None:
                        results.append(signal.last_result)
                    break
                except RestartLoopSignal as signal:
                    # Collect any result that was produced before restart-loop
                    if hasattr(signal, 'last_result') and signal.last_result is not None:
                        results.append(signal.last_result)
                    # Move to next iteration (restart current iteration)
                    i += 1
                    continue

            return results

    if isinstance(node, EndLoopStatement):
        # If we're not in a loop context, this is an error
        if not is_loop_context:
            raise EnzoRuntimeError("error: `end-loop;` inside a non-loop function atom", code_line=node.code_line)
        # Otherwise raise signal to break out of nearest loop
        raise EndLoopSignal()

    if isinstance(node, RestartLoopStatement):
        # If we're not in a loop context, this is an error
        if not is_loop_context:
            raise EnzoRuntimeError("error: `restart-loop;` inside a non-loop function atom", code_line=node.code_line)
        # Otherwise raise signal to restart nearest loop
        raise RestartLoopSignal()

    if isinstance(node, ComparisonExpression):
        left_val = eval_ast(node.left, value_demand=True, env=env)

        # Special handling for type comparisons with 'is' and 'is not'
        if ((node.operator == "is" or node.operator == "is not") and
            isinstance(node.right, VarInvoke) and
            node.right.name in ["Number", "Text", "List", "Empty"]):
            # Pass the type name directly instead of evaluating as a variable
            right_val = node.right.name
        else:
            right_val = eval_ast(node.right, value_demand=True, env=env)

        return _compare_values(left_val, node.operator, right_val)

    if isinstance(node, LogicalExpression):
        left_val = eval_ast(node.left, env=env)
        if node.operator == "and":
            if not _is_truthy(left_val):
                return left_val  # Short-circuit
            return eval_ast(node.right, env=env)
        elif node.operator == "or":
            if _is_truthy(left_val):
                return left_val  # Short-circuit
            return eval_ast(node.right, env=env)
        else:
            raise EnzoRuntimeError(f"Unknown logical operator: {node.operator}", code_line=code_line)

    if isinstance(node, NotExpression):
        operand_val = eval_ast(node.operand, env=env)
        return not _is_truthy(operand_val)

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

def _is_truthy(value):
    """Determine if a value is truthy in Enzo's boolean context"""
    if value is None or isinstance(value, Empty):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value != ""
    if isinstance(value, list):
        # A list is falsy if it's empty or contains only falsy values
        if len(value) == 0:
            return False
        return any(_is_truthy(item) for item in value)
    if isinstance(value, EnzoList):
        # A list is falsy if it's empty or contains only falsy values
        if len(value) == 0:
            return False
        return any(_is_truthy(item) for item in value)
    if isinstance(value, EnzoVariantInstance):
        # Check for specific falsy variants
        if value.group_name == "False" or (value.group_name == "Status" and value.variant_name == "False"):
            return False
        return True
    if isinstance(value, EnzoVariantGroup):
        # A variant group is falsy only if it's the False group
        if value.name == "False":
            return False
        return True
    if isinstance(value, EnzoFunction):
        # A function is truthy only if it has body statements and would return a truthy value
        if not value.body:
            return False  # Empty function is falsy

        # Evaluate the function to check its return value
        try:
            # Create a temporary environment for function evaluation
            temp_env = {}
            result = None
            for stmt in value.body:
                result = eval_ast(stmt, env=temp_env)
            # Function is truthy if its result is truthy
            return _is_truthy(result) if result is not None else False
        except:
            # If evaluation fails, assume truthy (non-empty function)
            return True
    # Handle built-in False constant
    if hasattr(value, '__class__') and value.__class__.__name__ == 'False':
        return False
    return bool(value)

def _compare_values(left, operator, right):
    """Compare two values using the given operator"""
    if operator == "is":
        # Type and value comparison
        if isinstance(right, str) and right in ["Number", "Text", "List", "Empty"]:
            # Type checking
            if right == "Number":
                return isinstance(left, (int, float))
            elif right == "Text":
                return isinstance(left, str)
            elif right == "List":
                return isinstance(left, (list, EnzoList))
            elif right == "Empty":
                return left is None or isinstance(left, Empty)
        # Value comparison
        return left == right
    elif operator == "is not":
        # Type and value comparison (opposite of "is")
        if isinstance(right, str) and right in ["Number", "Text", "List", "Empty"]:
            # Type checking
            if right == "Number":
                return not isinstance(left, (int, float))
            elif right == "Text":
                return not isinstance(left, str)
            elif right == "List":
                return not isinstance(left, (list, EnzoList))
            elif right == "Empty":
                return not (left is None or isinstance(left, Empty))
        # Value comparison
        return left != right
    elif operator == "is less than":
        if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
            from src.error_messaging import error_message_invalid_comparison_type
            raise EnzoRuntimeError(error_message_invalid_comparison_type())
        return left < right
    elif operator == "is greater than":
        if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
            from src.error_messaging import error_message_invalid_comparison_type
            raise EnzoRuntimeError(error_message_invalid_comparison_type())
        return left > right
    elif operator == "is at most":
        if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
            from src.error_messaging import error_message_invalid_comparison_type
            raise EnzoRuntimeError(error_message_invalid_comparison_type())
        return left <= right
    elif operator == "is at least":
        if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
            from src.error_messaging import error_message_invalid_comparison_type
            raise EnzoRuntimeError(error_message_invalid_comparison_type())
        return left >= right
    elif operator == "contains":
        if not isinstance(left, (list, EnzoList)):
            from src.error_messaging import error_message_contains_non_list
            raise EnzoRuntimeError(error_message_contains_non_list())
        return _contains_value(left, right)
    else:
        raise EnzoRuntimeError(f"Unknown comparison operator: {operator}")

def _contains_value(container, value):
    """Check if container contains value"""
    if isinstance(container, (list, EnzoList)):
        if isinstance(container, EnzoList):
            # Iterate through the EnzoList's elements
            for item in container:
                if item == value:
                    return True
            return False
        else:
            return value in container
    return False
