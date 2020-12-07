# To change config, check the config/config.json file

# Modules
from json import loads
from presence import crash

# Configuration class
class Config:

    def __init__(self):
        self.config = loads(open("config/config.json", "r").read())

    def __getitem__(self, key):
        if key not in self.config:
            crash(f"No key was found in the configuration that matched '{key}'. Please consult the documentation.")
        return self.config[key]
