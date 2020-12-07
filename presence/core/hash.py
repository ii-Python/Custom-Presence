# Modules
import string
import random
import hashlib

# Generate secrets
def generate_base():
    return "".join(str(random.choice(string.digits)) for _ in range(0, 26))

def generate_key():
    return hashlib.sha256(generate_base().encode("UTF-8")).hexdigest()
