import sys
import os
from colorama import init, Fore, Back, Style



# Initialize colorama for cross-platform color support
init(autoreset=True)

# Only color when stdout is a TTY (and NO_COLOR isn't set)
# Use the de facto NO_COLOR convention: if NO_COLOR is present, no color
use_color = sys.stdout.isatty() and ("NO_COLOR" not in os.environ)

BLACK_BG, WHITE, RESET = "\033[40m", "\033[97m", "\033[0m"

def color_error(msg):
    if not use_color:
        return msg
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"

def color_code(line: str) -> str:
    if not use_color:
        return line
    return f"{BLACK_BG}{WHITE}{line}{Style.RESET_ALL}"

# --- Additional color helpers for other scripts (optional) ---

def color_info(msg: str) -> str:
    if not use_color:
        return msg
    return f"{Fore.BLUE}{Style.BRIGHT}{msg}{Style.RESET_ALL}"

def color_diff(line: str) -> str:
    if not use_color:
        return line
    if line.startswith('-'):
        return f"{Fore.RED}{line}{Style.RESET_ALL}"       # Red for deletions
    if line.startswith('+'):
        return f"{Fore.GREEN}{line}{Style.RESET_ALL}"     # Green for additions
    if line.startswith('@@'):
        return f"{Fore.YELLOW}{Style.BRIGHT}{line}{Style.RESET_ALL}"     # Yellow for hunk headers
    return line

def color_test_title(msg: str) -> str:
    if not use_color:
        return msg
    return f"{Fore.MAGENTA}{msg}{Style.RESET_ALL}"

def color_block_title(msg: str) -> str:
    if not use_color:
        return msg
    return f"{Fore.BLUE}{msg}{Style.RESET_ALL}"

def color_actual_header(msg: str) -> str:
    if not use_color:
        return msg
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"

def color_expected_header(msg: str) -> str:
    if not use_color:
        return msg
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"

def color_red(msg: str) -> str:
    if not use_color:
        return msg
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"

def color_checkmark(line: str) -> str:
    if not use_color:
        return line
    if line.startswith('✔'):
        return f"{Fore.GREEN}{line}{Style.RESET_ALL}"
    if line.startswith('✖'):
        return f"{Fore.RED}{line}{Style.RESET_ALL}"
    return line