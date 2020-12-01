# Modules
import os
import sys

import json
import psutil

from ..colors import colored

def has_command(cmd):

    if cmd in sys.argv:
        return True

    lt = cmd[2:]
    lt = lt[0].upper()

    if f"-{lt}" in sys.argv:
        return True

    return False

def run_commands():

    # Help command
    if has_command("--setup"):

        running = []
        for proc in psutil.process_iter():
            
            name = proc.name().replace(".exe", "")

            if name not in running:
                running.append(name)

        print(colored("So, you want to setup a new application for the status changer.", "green"))
        print(colored("In short, it should follow the following syntax:", "green"))
        print(colored(json.dumps({"APPEXE_NAME": {"text": "Small Text", "longName": "Full Application Name"}}, indent = 4), "yellow"))
        print()
        print(colored("For the APPEXE_NAME, you should choose the one you want from the list (make sure the app you want is running):", "green"))
        print(colored("".join(p + ", " for p in running)[:-2], "yellow"))
        print()
        print(colored("This is important! Make sure you go to https://discord.com/developers/applications/APP_ID/rich-presence/assets", "green"))
        print(colored("and make sure you upload an image for your application. Its name must be the all-lowercase form of APPEXE_NAME.", "green"))
        exit()

    # Update script
    if has_command("--update"):

        print(colored("Custom Presence - Automatic Update Script", "yellow"))
        print()

        print(colored("Saving config file to memory...", "yellow"))
        config = open("config.py", "r").read()
        print(colored("  saved!", "green"))

        print(colored("Stashing stages...", "yellow"))
        os.system("git stash")
        print(colored("  done!", "green"))

        print(colored("Cloning update (using origin remote)...", "yellow"))
        os.system("git pull origin master")
        print(colored("  done!", "green"))

        print(colored("Reverting to old configuration...", "yellow"))
        open("config.py", "w").write(config)
        print(colored("  done!", "green"))

        print(colored("Installing dependencies (requirements.txt)...", "yellow"))
        os.system("python -m pip install -r requirements.txt")
        print(colored("  done!", "green"))

        print()

        print(colored("Update has been completed!", "green"))
        exit()
