# Modules
import os
import sys

import time
import pypresence

from ..utils.errors import errors
from ..utils.colors import colored

from .chromium import get_chromium_website
from ..utils.logging import crash, verbose, info

# Presence class
class CustomPresence(pypresence.Presence):

    def __init__(self, config, pipe = 0):
        super().__init__(config["app_id"], pipe = pipe)

        self.config = config

        self.prev_app = None
        self.prev_time = None

    def kill(self, ctrl = True):

        verbose("Shutting down script...")
        self.close()  # Close the RPC connection to allow other statuses

        # Remove RPC dump (for security purposes)
        if "--keep-rpc" not in sys.argv:

            try:
                os.remove("rpc.json")

            except (PermissionError, FileNotFoundError):
                pass

            except Exception as err:
                verbose("Failed to remove RPC dump with error", err)

        # Print & exit
        if ctrl:
            info(colored("Status changer stopped via CTRL+C.", "red"))

        exit()

    def establish(self, keys):
        self.keys = keys

        try:
            self.connect()

        except (ConnectionRefusedError, pypresence.exceptions.InvalidPipe):
            crash(errors["FailedConnect"])

    def previous_time(self, app):

        verbose("Checking the validity of stored elapsed time...")
        if not self.prev_app:
            self.prev_app = app

        if self.prev_time:
            if self.prev_app != app:
                self.prev_app = app
                self.prev_time = self.time()
                verbose("  revalidated time!")
            else:
                verbose("  time is still valid.")

            return self.prev_time

        self.prev_time = self.time()
        return self.prev_time

    def set_status(self, app):

        # Chromium browsers
        if app.endswith("|CSPRC_CHROMIUM"):
            name, app = get_chromium_website(self.config, app)

            if name is None or app is None:
                return

        else:
            name = app
            app = self.config["applications"][app]

        # Lobby data
        lobby = {}

        if self.config["allowJoining"]:
            lobby = {
                "join": self.keys["join"],
                "party_id": self.keys["party"],
                "party_size": [1, self.config["maxJoinSize"]]
            }

        # Elapsed time
        elapsed = {}
        if self.config["showElapsed"]:
            elapsed["start"] = self.previous_time(app)

        # Update our presence
        try:
            self.dump = self.update(
                # State information
                details = app["name"],
                state = app["text"],
                # Images
                large_image = name,
                large_text = app["name"],
                small_image = self.config["smallImage"],
                small_text = self.config["hoverText"],
                # Game and lobbies
                **lobby,
                # Time
                **elapsed
            )
        except pypresence.exceptions.InvalidID:
            crash("Discord was closed while the status was running.")
            self.kill(ctrl = False)
        except KeyboardInterrupt:
            self.kill()

        return self.dump

    @staticmethod
    def time():

        return round(time.time())
