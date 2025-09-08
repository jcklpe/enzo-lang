"""
Simple Enzo setup for debugging notebook issues
"""

def simple_enzo_setup():
    """Simple setup without complex autoreload that might cause traitlets issues"""

    # Import Enzo components
    from src.evaluator import eval_ast, _env, _initialize_builtin_variants
    from src.enzo_parser.parser import parse
    from IPython.core.magic import register_cell_magic

    # Create simple magic commands
    @register_cell_magic
    def enzo(line, cell):
        """Execute Enzo code in a cell"""
        try:
            ast = parse(cell)
            result = eval_ast(ast)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"❌ Error: {e}")

    @register_cell_magic
    def enzo_fresh(line, cell):
        """Execute Enzo code with a fresh environment"""
        try:
            # Reset environment but preserve built-ins
            _env.clear()
            _initialize_builtin_variants()

            ast = parse(cell)
            result = eval_ast(ast)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"❌ Error: {e}")

    # Initialize the environment
    _env.clear()
    _initialize_builtin_variants()

    print("✅ Simple Enzo setup complete! Use %%enzo or %%enzo_fresh magic commands.")
    return parse, eval_ast

def setup_enzo_with_autoreload():
    """Fallback that uses simple setup"""
    print("🔄 Using simple setup to avoid traitlets issues...")
    return simple_enzo_setup()
