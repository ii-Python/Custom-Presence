# Modules
import os

# Initialization
colors = {
    "red": "\033[91m",
    "green": "\033[92m",
    "cyan": "\033[36m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "reset": "\033[0m"
}

# Colored function
def colored(text, color):
    return colors[color] + text + colors["reset"]

# Clear the screen
def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        raise SystemError("Unknown or unsupported operating system! Sorry :(")
