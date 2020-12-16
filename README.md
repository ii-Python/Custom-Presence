# Custom Presence
### a small RPC presence program designed for customizability
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org) [![GitHub license](https://img.shields.io/github/license/ii-Python/Custom-Presence.svg)](https://github.com/ii-Python/Custom-Presence/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/release/ii-Python/Custom-Presence.svg)](https://github.com/ii-Python/Custom-Presence/releases/) [![Only 9 Kb](https://badge-size.herokuapp.com/ii-Python/Custom-Presence/master/presence/core/rpc.py)](https://github.com/ii-Python/Custom-Presence/blob/master/presence/core/rpc.py) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/ii-Python/Custom-Presence) [![Discord](https://img.shields.io/discord/783364354040528916.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/dHMjBRbwhs)
---

Custom Presence is a python program that utilizes the Discord RPC to make a custom status.
Built completely on `pypresence` as well as `psutil`; it also requires `colorama` for full color support.

## Install
---
To install Custom Presence you require Python 3.6+ (3.8+ is recommended).

**Using Git (recommended method):**
  - Clone the repository with `git clone https://github.com/ii-Python/Custom-Presence.git && cd Custom-Presence`
  - Install the required dependencies with `python3 -m pip install -r requirements.txt`.

**Linux systems:**
  - In addition to the above steps, you will also need to run `sudo apt-get install xdotool`.

Following completion, you can run the script with `python3 main.py`.

The script also comes with a built-in update script, available via `python3 main.py --update`.

## Documentation
---

Custom Presence is meant to be completely customizable, and with that said it is.
The `config/config.json` file contains all of the data that the script uses and `config/values.txt` explains all of the json file values. You can change the application ID (in case you have your own), the refresh rate, the applications, whether to enable chrome rich presence, toggle joining, etc.

For more information please check out `config/values.txt`.

#### CLI Syntax
---
Custom Presence has the following syntax:
```
main.py [options]
```

Provided is a list of available options:
  - `--show-keys`, which prints the join and party key
  - `--keep-rpc`, which stops the script from deleting `rpc.json` on exit

### Troubleshooting
---

"Something went wrong while loading the configuration":
  - Make sure that `config.py` exists and is a valid Python file and is importable.
  - Make sure there are no syntax errors
  - Make sure that the `Config` class exists and is callable.

"updateTime needs to be at least a 15 second interval":
  - Set `updateTime` to a value bigger than (or equal to) 15 (the required RPC delay).
