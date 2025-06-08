import sys, os

# only color when stdout is a TTY (and NO_COLOR isn't set)
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
