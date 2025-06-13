import sys
import os

# Only color when stdout is a TTY (and NO_COLOR isn't set)
use_color = (os.getenv("NO_COLOR") is None) and sys.stdout.isatty()

def color_error(msg: str) -> str:
    if not use_color:
        return msg
    RED, RESET = "\033[91m", "\033[0m"
    return f"{RED}{msg}{RESET}"

def color_code(line: str) -> str:
    if not use_color:
        return line
    BLACK_BG, WHITE, RESET = "\033[40m", "\033[97m", "\033[0m"
    return f"{BLACK_BG}{WHITE}{line}{RESET}"

# --- Additional color helpers for other scripts (optional) ---

def color_info(msg: str) -> str:
    if not use_color:
        return msg
    BLUE, RESET = "\033[94;1m", "\033[0m"
    return f"{BLUE}{msg}{RESET}"

def color_diff(line: str) -> str:
    if not use_color:
        return line
    if line.startswith('-'):
        return f"\033[91m{line}\033[0m"       # Red for deletions
    if line.startswith('+'):
        return f"\033[94;1m{line}\033[0m"     # Blue for additions
    if line.startswith('@@'):
        return f"\033[93;1m{line}\033[0m"     # Yellow for hunk headers
    return line
