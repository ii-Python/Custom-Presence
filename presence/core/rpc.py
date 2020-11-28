# Modules
import os
import sys

import time
import json

import psutil
import random

import colorama
import pypresence

from ..colors import colored
from .hash import generate_key

from ..logging import crash, info

# Client class
class Client(pypresence.Presence):

    def __init__(self, config, host, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config

        try:
            self.join_key = generate_key(self.config)
            self.party_id = generate_key(self.config)
        except TypeError:
            crash("The secretLib used is not valid in the context required. Please check the documentation.")

        try:
            self.connect()
        except pypresence.exceptions.InvalidPipe:
            crash("Discord is not running!")

        # Information
        info(colored("The status changer has been started.", "blue"))
        info(colored("Press CTRL+C at any time to stop it.", "blue"))
        info(colored("Thanks for using it! :D", "blue"))

        print()
        info(colored(host.__copyright__, "blue"))
        info(colored(f"Running RPC v{host.__version__}", "blue"))
        print()

        info(colored("Keys generated (don't share these!):", "yellow"))
        info(colored(f"  Join key: {self.join_key}", "yellow"))
        info(colored(f"  Party ID: {self.party_id}", "yellow"))

    def init(self):

        # Initialize colorama
        colorama.init()

        # Help command
        if "--setup" in sys.argv:

            running = []
            for proc in psutil.process_iter():
                
                name = proc.name().replace(".exe", "")

                if name not in running:
                    running.append(name)

            print(colored("So, you want to setup a new application for the status changer.", "green"))
            print(colored("In short, it should follow the following syntax:", "green"))
            print(colored(dumps({"APPEXE_NAME": {"text": "Small Text", "longName": "Full Application Name"}}, indent = 4), "yellow"))
            print()
            print(colored("For the APPEXE_NAME, you should choose the one you want from the list (make sure the app you want is running):", "green"))
            print(colored("".join(p + ", " for p in running)[:-2], "yellow"))
            print()
            print(colored(f"This is important! Make sure you go to https://discord.com/developers/applications/{self.config['app_id']}/rich-presence/assets", "green"))
            print(colored("and make sure you upload an image for your application. Its name must be the all-lowercase form of APPEXE_NAME.", "green"))
            exit()

    def get_app(self):

        running = []

        for program in psutil.process_iter():

            name = program.name().replace(".exe", "")
            if name in running: continue

            if name in self.config["applications"]:
                running.append(name)

        if not running:
            return None

        app = random.choice(running) if self.config["forceApp"] is None else self.config["forceApp"]
        return app

    def kill(self):

        self.close()  # Close the RPC connection to allow other statuses
        
        # Remove RPC dump (for security purposes)
        if "--keep-rpc" not in sys.argv:
            try: os.remove("rpc.json")
            except PermissionError: pass
            except FileNotFoundError: pass

        # Print & exit
        info(colored("Status changer stopped via CTRL+C.", "red"))
        exit()

    def wait(self, extraDelay: int = 0):

        try: time.sleep(self.config["updateTime"] + extraDelay)
        except KeyboardInterrupt: self.kill()

    def set_presence(self, app):

        if app is None:
            return info(colored("No applications in the database currently running (skipping turn)", "red"))

        data = self.config["applications"][app]

        # Update our presence
        lobby = {}

        if self.config["allowJoining"]:
            lobby = {
                "join": self.join_key,
                "party_id": self.party_id,
                "party_size": [1, self.config["maxJoinSize"]]
            }

        try:
            r = self.update(
                # State information
                details = data["longName"],
                state = data["text"],
                # Images
                large_image = app.lower(),
                large_text = data["longName"],
                small_image = self.config["smallImage"],
                small_text = self.config["hoverText"],
                # Game and lobbies
                **lobby
            )
        except pypresence.exceptions.InvalidID:
            crash("Discord was closed while the status was running.")
        except KeyboardInterrupt:
            self.kill()

        open("rpc.json", "w+").write(json.dumps(r, indent = self.config["indentSize"]))
        info(colored(f"RPC information dumped to rpc.json (refreshing in {self.config['updateTime']} seconds(s))", "green"))
