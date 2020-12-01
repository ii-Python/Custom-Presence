# Modules
import os
import sys

import time
import json

import psutil
import win32gui

import pypresence
import win32process

from random import choice
from .web import websites

from .hash import generate_key
from ..colors import colored, clear

from ..scripts.cmd import run_commands
from ..logging import crash, info, verbose

# Client class
class Client(pypresence.Presence):

    def __init__(self, config, host, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clear()  # Nice effect, right?

        info(colored(host.__copyright__, "blue"))
        info(colored(f"Running RPC v{host.__version__}", "blue"))
        print()

        self.config = config
        self.prev_time = None
        self.prev_app = None

        try:
            self.join_key = generate_key(self.config)
            self.party_id = generate_key(self.config)
        except TypeError:
            crash("The secretLib used is not valid in the context required. Please check the documentation.")

        try:
            info(colored("Starting Custom Presence...", "green"))
            self.connect()
        except pypresence.exceptions.InvalidPipe:
            crash("Discord is not running!")

        # Information
        print()

        info(colored("The status changer has been started; press CTRL+C at any time to stop it.", "blue"))
        info(colored("Thanks for using Custom Presence, feel free to support the project! :D", "blue"))

        print()

        if "--show-keys" in sys.argv:
            info(colored("Keys generated (don't share these!):", "yellow"))
            info(colored(f"  Join key: {self.join_key}", "yellow"))
            info(colored(f"  Party ID: {self.party_id}", "yellow"))

    def _rich_google_status(self, title):

        app = "chrome"
        data = self.config["applications"]["chrome"]

        website = "".join(piece + " - " for piece in title.split(" - ")[:-1])[:-3]
        page = ""

        if " - " in website:
            cut = website.rsplit(" - ")

            page = "".join(piece + " - " for piece in cut[:-1])[:-3]
            website = website.rsplit(" - ")[-1]

        # Rich presence
        if website in websites:

            website = websites[website]
            text = website["text"].format(page)
            if text != "":

                app = website["icon_name"]

                data = {
                    "text": text,
                    "longName": website["name"]
                }

        return (app, data)

    def time(self):

        return round(time.time())

    def previous_time(self, app):

        if not self.prev_app:
            self.prev_app = app

        if self.prev_time:
            if self.prev_app != app:
                self.prev_app = app
                self.prev_time = self.time()
            return self.prev_time

        self.prev_time = self.time()
        return self.prev_time

    def init(self):
        run_commands()

        # todo: add some sort of clock here idk

    def get_bg_apps(self):

        running = []
        for program in psutil.process_iter():
            name = program.name().replace(".exe", "")
            if name in running: continue
            if name in self.config["applications"]:
                running.append(name)

        return running

    def get_app(self):

        app = win32gui.GetForegroundWindow()
        verbose("Located app", app, "as the foreground window.")

        try:
            pid = win32process.GetWindowThreadProcessId(app)
            process = psutil.Process(pid[-1])
        except [psutil.NoSuchProcess, ValueError] as err:
            verbose("Failed to fetch process info for", app, "with", err)
            return None  # Callback for when a process is quickly closed or for the desktop sometimes

        name = process.name().replace(".exe", "")
        if name is None:
            verbose("For some reason no app name was received.")
            return None

        name = name if self.config["forceApp"] is None else self.config["forceApp"]

        # Check our program weight
        if self.config["useWeight"]:
            if name in self.config["applications"]:
                _ = self.config["applications"][name]
                if _["weight"] == 0:

                    # Prefer to seek out a background task
                    verbose("Searching for tasks with a higher weight then 1...")

                    rn = self.get_bg_apps()
                    running = []
                    for _rn in rn:
                        if self.config["applications"][_rn]["weight"] > 0:
                            verbose(" ", "found app", _rn, "with weight of", self.config["applications"][_rn]["weight"])
                            running.append(_rn)

                    if running:
                        name = choice(running)
                        verbose("Chose", name, "as the weighted background app!")
                        if not self.prev_app or self.prev_app != name:
                            info(colored(f"The {name} application is running and will override other applications.", "green"))

        # This really isn't a valid app, seek out something else
        if not name in self.config["applications"]:
            apps = self.get_bg_apps()
            if apps:

                # We are able to set the name since chrome is the only
                # app that depends on GetWindowText, instead of others.

                # By default chrome would have a weight higher than 0 to
                # prevent issues, if not file a bug report.
                name = choice(apps)

        return (name, win32gui.GetWindowText(app))

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

        if self.config["updateTime"] < 15:
            crash("updateTime needs to be at least a 15 second interval!")

        try: time.sleep(self.config["updateTime"] + extraDelay)
        except KeyboardInterrupt: self.kill()

    def set_presence(self, app):

        name = app[0]
        title = app[1]

        app = name

        if app is None or not app in self.config["applications"]:
            return info(colored("No applications in the database currently running (skipping turn)", "red"))

        data = self.config["applications"][app]

        # Google chrome rich status
        if app == "chrome":
            (app, data) = self._rich_google_status(title)

        # Lobby data
        lobby = {}

        if self.config["allowJoining"]:
            lobby = {
                "join": self.join_key,
                "party_id": self.party_id,
                "party_size": [1, self.config["maxJoinSize"]]
            }

        # Experimental time
        time = {}
        if self.config["showElapsed"]:
            time["start"] = self.previous_time(app)

        # Update our presence
        try:
            r = self.update(
                # State information
                details = data["longName"],
                state = data["text"],
                # Images
                large_image = app.lower().replace(" ", ""),
                large_text = data["longName"],
                small_image = self.config["smallImage"],
                small_text = self.config["hoverText"],
                # Experimental time
                **time,
                # Game and lobbies
                **lobby
            )
        except pypresence.exceptions.InvalidID:
            crash("Discord was closed while the status was running.")
        except KeyboardInterrupt:
            self.kill()

        open("rpc.json", "w+").write(json.dumps(r, indent = self.config["indentSize"]))
        if "--show-rpc-dump" in sys.argv: 
            info(colored(f"RPC information dumped to rpc.json (refreshing in {self.config['updateTime']} seconds(s))", "green"))
