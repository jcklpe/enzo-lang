# src/color_helpers.py

from colorama import Fore, Style, Back

def color_error(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def color_code(text):
    return f"{Back.BLACK}{Fore.WHITE}{text}{Style.RESET_ALL}"
