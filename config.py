# Modules
import hashlib
from presence import crash

# Configuration
configuration = {
    "app_id": "781764116188495882",  # Make sure this is a string
    "updateTime": 15,  # The amount of time before the status is refreshed
    "applications": {  # The applications you want for the status to display
        # "text" represents the second-line of text displayed
        # "longName" represents the title line on the status
        # "weight" respresents the "weight" of the application
        #    - 0 represents the app must be focused
        #    - 1 represents the app is a background process
        "Code": {
            "text": "Programming something",
            "longName": "Visual Studio Code",
            "weight": 0
        },
        "chrome": {
            "text": "Exploring the web",
            "longName": "Google Chrome",
            "weight": 0
        },
        "Discord": {
            "text": "Talking to someone",
            "longName": "Discord",
            "weight": 0
        },
        "Spotify": {
            "text": "Listening to music",
            "longName": "Spotify",
            "weight": 1
        },
        "RobloxPlayerBeta": {
            "text": "Playing a game",
            "longName": "Roblox Player",
            "weight": 0
        },
        "Twitch": {
            "text": "Watching a stream",
            "longName": "Twitch",
            "weight": 0
        },
        "MinecraftLauncher": {
            "text": "Playing Minecraft",
            "longName": "Minecraft",
            "weight": 0
        },
        "msedge": {
            "text": "Browsing the web",
            "longName": "Microsoft Edge",
            "weight": 0
        },
        "steam": {
            "text": "Exploring steam",
            "longName": "Steam",
            "weight": 0
        },
        "Among Us": {
            "text": "Playing in a round",
            "longName": "Among Us",
            "weight": 0
        }
    },
    "hoverText": "Ben's Custom Status",  # The text that shows when you hover over the image
    "indentSize": 4,  # The indentation level of rpc.json
    "forceApp": None,  # The name of an application to force
    "smallImage": "goose",  # The image to use as a small icon
    "secretLib": hashlib.sha256,  # The hash function to use for generating secrets (use sha526 if you don't know what this does)
    "maxJoinSize": 6,  # The maximum amount of people that can join your "activity"
    "allowJoining": False,  # Whether to display a "Join" button on your status or not
    "showElapsed": True,  # Whether or not to display the "00:00 elapsed" text on your status
    "useWeight": True  # Whether or not to display applications based on their weight
}

class Config:

    def __init__(self):
        self.config = configuration

    def __getitem__(self, key):
        if key not in self.config:
            crash(f"No key was found in the configuration that matched '{key}'. Please consult the documentation.")
        return self.config[key]
