"""
Enzo Language Universal Setup
Simple one-line setup for both local and Google Colab environments
"""

def setup_enzo():
    """Universal Enzo setup that works in both local and Colab environments"""

    # Check if we're in Google Colab
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

    if IN_COLAB:
        # Google Colab setup
        import os
        import sys

        # Clone the repository if it doesn't exist
        if not os.path.exists("enzo-lang"):
            os.system("git clone https://github.com/jcklpe/enzo-lang.git > /dev/null 2>&1")

        # Add to Python path
        sys.path.insert(0, '/content/enzo-lang/interpreter')

        # Install required dependencies quietly
        os.system("pip install lark --quiet > /dev/null 2>&1")

        # Import Enzo components
        from src.evaluator import eval_ast, _env, _initialize_builtin_variants
        from src.enzo_parser.parser import parse
        from IPython.core.magic import register_cell_magic

        # Create magic commands for Colab
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

        print("✅ Enzo ready! Use %%enzo or %%enzo_fresh magic commands.")
        return parse, eval_ast

    else:
        # Local environment setup
        try:
            # Try the original setup first
            from enzo_notebook_setup import setup_enzo_with_autoreload
            return setup_enzo_with_autoreload()
        except Exception:
            # Fallback to simple setup
            from simple_enzo_setup import simple_enzo_setup
            return simple_enzo_setup()

# Convenience function for one-line import
def quick_setup():
    """One-line setup function"""
    return setup_enzo()
