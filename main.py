# Copyright 2020; Benjamin O'Brien (iiPython)
# Under the MIT license, see LICENSE for more information.

# Modules
import sys
import json

import presence
import colorama

try:
    from config import Config
    config = Config()
except ImportError:
    presence.crash("Something went wrong while loading the configuration. Please consult the documentation.")

# Initialize commands
presence.run_commands()

# Initialize colorama
info = presence.info
colored = presence.colored

colorama.init()
presence.clear()  # Clear the screen for effect

# Initialize RPC
info(colored("Starting Custom Presence...", "green"))

rpc = presence.RPC.Client(config, config["app_id"])
rpc._connect()

# Information
presence.clear()  # Nice clear effect

info(colored(presence.__copyright__, "blue"))
info(colored(f"Running RPC v{presence.__version__}", "blue"))

print()

info(colored("The status changer has been started; press CTRL+C at any time to stop it.", "blue"))
info(colored("Thanks for using Custom Presence, feel free to support the project! :D", "blue"))

print()

# Join and party keys
if "--show-keys" in sys.argv:
    info(colored("Keys generated (don't share these!):", "yellow"))
    info(colored(f"  Join key: {rpc.join_key}", "yellow"))
    info(colored(f"  Party ID: {rpc.party_id}", "yellow"))

    print()

# Main loop
while True:

    app = rpc.get_app()
    rpc.set_presence(app)

    if "--show-rpc-dump" in sys.argv:
        open("rpc.json", "w+").write(json.dumps(rpc.dump, indent = config["indentSize"]))
        sec = config["updateTime"]

        info(colored(f"RPC information dumped to rpc.json (refreshing in {sec} seconds(s))", "green"))

    rpc.wait(0)
