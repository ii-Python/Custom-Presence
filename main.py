# Copyright 2020; Benjamin O'Brien (iiPython)
# Under the MIT license, see LICENSE for more information.

# Modules
import presence

try:
    from config import Config
    config = Config()
except ImportError:
    presence.crash("Something went wrong while loading the configuration. Please consult the documentation.")

# Initialization
rpc = presence.RPC.Client(config, presence, config["app_id"])

# Main loop
while True:

    app = rpc.get_app()
    rpc.set_presence(app)

    rpc.wait(0)
