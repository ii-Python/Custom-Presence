# Modules
import pypresence
from ..utils.logging import crash
from ..utils.errors import errors

# Presence class
class CustomPresence(pypresence.Presence):

    def __init__(self, config):
        super().__init__(config["app_id"])

    def kill(self):
        ass

    def establish(self):
        try:
            self.connect()
        except ConnectionRefusedError:
            crash(errors["FailedConnect"])
        except pypresence.exceptions.InvalidPipe:
            crash(errors["FailedConnect"])
