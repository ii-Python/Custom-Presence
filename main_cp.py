# Copyright 2020; Benjamin O'Brien (iiPython)
# Under the MIT license, see LICENSE for more information.

# Modules
import sys
import colorama

import presence_cp
from time import sleep

# Load configuration
try:
    from config import Config
    config = Config()

except ImportError:
    presence_cp.crash("Something went wrong while loading the configuration.")

# Initialization
colorama.init()
rpc = presence_cp.RPC(config)

keys = {
    "join": presence_cp.generate_key(),
    "party": presence_cp.generate_key()
}

# Establish connection
info = presence_cp.info
colored = presence_cp.colored

info(colored("Starting Custom Presence...", "green"))
rpc.establish()

# Information
presence_cp.clear()  # Nice clear effect

info(colored(presence_cp.__copyright__, "blue"))
info(colored(f"Running Custom Presence v{presence_cp.__version__}", "blue"))

print()

info(colored("The program has been started; press CTRL+C at any time to stop it.", "blue"))
info(colored("Thanks for using Custom Presence, feel free to support the project! :D", "blue"))

print()

# Master loop
app_handler = presence_cp.ApplicationHandler(rpc)
while True:

    # Locate the running app
    app = app_handler.locate_app()
    print(app)

    # RPC update interval
    sleep(config["updateTime"])
