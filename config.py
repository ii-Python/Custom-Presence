# Modules
import hashlib
from presence import crash

# Configuration
configuration = {
    "app_id": "781764116188495882",  # Make sure this is a string
    "updateTime": 15,  # The amount of time before the status is refreshed
    "applications": {  # The applications you want for the status to display
        "Code": {
            "text": "Programming something",
            "longName": "Visual Studio Code"
        },
        "chrome": {
            "text": "Exploring the web",
            "longName": "Google Chrome"
        },
        "Discord": {
            "text": "Talking to someone",
            "longName": "Discord"
        },
        "Spotify": {
            "text": "Listening to music",
            "longName": "Spotify"
        },
        "RobloxPlayerBeta": {
            "text": "Playing a game",
            "longName": "Roblox Player"
        }
    },
    "hoverText": "Ben's Custom Status",  # The text that shows when you hover over the image
    "indentSize": 4,  # The indentation level of rpc.json
    "forceApp": None,  # The name of an application to force
    "smallImage": "goose",  # The image to use as a small icon
    "secretLib": hashlib.sha256,  # The hash function to use for generating secrets (use sha526 if you don't know what this does)
    "maxJoinSize": 6,  # The maximum amount of people that can join your "activity"
    "allowJoining": False  # Whether to display a "Join" button on your status or not
}

class Config:

    def __init__(self):
        self.config = configuration

    def __getitem__(self, key):
        if key not in self.config:
            crash(f"No key was found in the configuration that matched '{key}'. Please consult the documentation.")
        return self.config[key]
