# Modules
from .colors import colored
from datetime import datetime

# Logging functions
def info(m):

    time = datetime.now().strftime("%I:%M:%S %p")
    print(colored(f"[{time}]:", "yellow"), m)

def crash(m):

    info(colored(m, "red"))
    exit()
