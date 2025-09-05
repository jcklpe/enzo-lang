"""
Enzo Language Notebook Setup Module

This module provides setup functionality for Jupyter notebooks that want to use
the Enzo language interpreter. It handles environment detection, dependency
installation, and magic command registration.

Usage:
    from enzo_notebook_setup import setup_enzo
    setup_enzo()
"""

import sys
import os
import shutil
from IPython.core.magic import register_line_cell_magic, register_line_magic

# Module-level globals for Enzo components
_enzo_parse = None
_enzo_eval_ast = None
_enzo_env = None
_enzo_init_builtins = None


def setup_enzo(force_reload=False):
    """
    Setup the Enzo language interpreter for use in Jupyter notebooks.

    Args:
        force_reload (bool): If True, forces a reload of Enzo modules even if already loaded

    Returns:
        tuple: (parse function, eval_ast function) for direct use if needed
    """

    # Check if we are in Google Colab
    try:
        import google.colab
        IN_COLAB = True
        print("🌐 Detected Google Colab environment")
    except ImportError:
        IN_COLAB = False
        print("💻 Detected local environment")

    # Clone the repository and install dependencies only if in Colab
    if IN_COLAB:
        print("📦 Installing dependencies...")
        os.system("pip install lark --quiet")

        if os.path.exists("enzo-lang"):
            shutil.rmtree("enzo-lang")
        os.system("git clone --depth 1 https://github.com/jcklpe/enzo-lang.git")

        enzo_src_path = "./enzo-lang/interpreter/src"
        if enzo_src_path not in sys.path:
            sys.path.insert(0, enzo_src_path)
        print("🔧 Enzo interpreter loaded from repository")
    else:
        # If running locally, assume the interpreter is in the correct path
        local_src_path = "./src"
        if local_src_path not in sys.path:
            sys.path.insert(0, local_src_path)
        print("🔧 Enzo interpreter loaded from local source")

    # Import or reload Enzo modules
    if force_reload or 'src.enzo_parser.parser' not in sys.modules:
        # Remove existing modules to force reload
        modules_to_remove = [mod for mod in sys.modules.keys() if mod.startswith('src.')]
        for mod in modules_to_remove:
            del sys.modules[mod]
        print("🔄 Reloading Enzo modules...")

    try:
        from src.enzo_parser.parser import parse
        from src.evaluator import eval_ast, _env, _initialize_builtin_variants
        print("✅ Enzo parser and evaluator loaded successfully")
    except ImportError as e:
        print(f"❌ Failed to import Enzo modules: {e}")
        return None, None

    # Store references for magic commands in module globals
    global _enzo_parse, _enzo_eval_ast, _enzo_env, _enzo_init_builtins
    _enzo_parse = parse
    _enzo_eval_ast = eval_ast
    _enzo_env = _env
    _enzo_init_builtins = _initialize_builtin_variants

    # Register the %%enzo magic command to execute Enzo code in cells
    @register_line_cell_magic
    def enzo(line, cell=None):
        """Magic command to execute Enzo code in Jupyter cells."""
        src = line if cell is None else cell
        try:
            result = _enzo_eval_ast(_enzo_parse(src), value_demand=True)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"❌ Error: {e}")

    # Register a magic command to reset the Enzo environment
    @register_line_magic
    def enzo_reset(line):
        """Magic command to reset the Enzo environment, clearing all variables."""
        try:
            _enzo_env.clear()
            _enzo_init_builtins()
            print("🧹 Enzo environment reset - all variables cleared")
        except Exception as e:
            print(f"❌ Error resetting environment: {e}")

    # Register a magic command that combines reset + execution
    @register_line_cell_magic
    def enzo_fresh(line, cell=None):
        """Magic command that resets environment then executes Enzo code."""
        src = line if cell is None else cell
        try:
            # Reset environment first
            _enzo_env.clear()
            _enzo_init_builtins()

            # Then execute the code
            result = _enzo_eval_ast(_enzo_parse(src), value_demand=True)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"❌ Error: {e}")

    print("🪄 Magic commands registered:")
    print("   %%enzo        - Execute Enzo code")
    print("   %enzo_reset   - Clear all Enzo variables")
    print("   %%enzo_fresh  - Reset environment then execute Enzo code")
    print("✅ Enzo setup complete!")
    print()
    print("Usage examples:")
    print("%%enzo")
    print('$greeting: "Hello, Enzo!";')
    print("$greeting;")
    print()
    print("%%enzo_fresh  # Starts with clean environment")
    print('$greeting: "Hello again!";')
    print("$greeting;")

    return parse, eval_ast


def reload_enzo():
    """
    Convenience function to reload the Enzo interpreter.
    Useful during development when you've made changes to the interpreter.
    """
    print("🔄 Reloading Enzo interpreter...")
    return setup_enzo(force_reload=True)


# Auto-reload functionality
def enable_autoreload():
    """
    Enable IPython's autoreload extension for automatic module reloading.
    This will automatically reload changed modules when cells are executed.
    """
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython:
            ipython.magic('load_ext autoreload')
            ipython.magic('autoreload 2')
            print("🔄 Auto-reload enabled - modules will be automatically reloaded when changed")
        else:
            print("⚠️  Not running in IPython environment - auto-reload not available")
    except Exception as e:
        print(f"⚠️  Could not enable auto-reload: {e}")


# Convenience function that sets up everything
def setup_enzo_with_autoreload():
    """
    Setup Enzo with auto-reload functionality enabled.
    This is the recommended setup for development work.
    """
    enable_autoreload()
    return setup_enzo()