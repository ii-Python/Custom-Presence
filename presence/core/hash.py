# Modules
import string
import random
from ..logging import crash

# Generate secrets
def generate_base():
    return "".join(str(random.choice(string.digits)) for _ in range(0, 26))

def generate_key(config):

    if config["secretLib"] is None:
        crash("secretLib needs to be set in order to use this! If you don't know what that is, set it to hashlib.sha256")

    return config["secretLib"](generate_base().encode("UTF-8")).hexdigest()
