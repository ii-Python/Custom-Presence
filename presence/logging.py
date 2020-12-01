# Modules
import sys
from .colors import colored
from datetime import datetime

# Logging functions
def info(m):

    time = datetime.now().strftime("%I:%M:%S %p")
    print(colored(f"[{time}]:", "yellow"), m)

def crash(m):

    info(colored(m, "red"))
    exit()

def verbose(*args):

    if "-v" not in sys.argv: return

    time = datetime.now().strftime("%D %I:%M:%S %p")
    print(colored(f"[{time} (VERBOSE)]:", "yellow"), *args)
