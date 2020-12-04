# Custom Presence
### a small RPC presence program designed for customizability
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org) [![GitHub license](https://img.shields.io/github/license/ii-Python/Custom-Presence.svg)](https://github.com/ii-Python/Custom-Presence/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/release/ii-Python/Custom-Presence.svg)](https://github.com/ii-Python/Custom-Presence/releases/) [![Only 9 Kb](https://badge-size.herokuapp.com/ii-Python/Custom-Presence/master/presence/core/rpc.py)](https://github.com/ii-Python/Custom-Presence/blob/master/presence/core/rpc.py) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/ii-Python/Custom-Presence) [![Discord](https://img.shields.io/discord/783364354040528916.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/dHMjBRbwhs)
---

Custom Presence is a python program that utilizes the Discord RPC to make a custom status.
It relies on `pypresence` as well as `psutil`; it also requires `colorama` for Windows color support.

## Install
---
To install Custom Presence you require Python 3.6+ (3.8+ is recommended).

**Using Git (recommended method):**
  - Clone the repository with `git clone https://github.com/ii-Python/Custom-Presence.git && cd Custom-Presence`
  - Install the required dependencies with `python -m pip install -r requirements.txt`.

Once installed, you can launch the presence with `python main.py`.

## Documentation
---

You can use `config.py` to setup custom programs, change refresh times, etc.

For a small example of adding a custom program to it, run `python main.py --setup` for instructions.


---
Custom Presence has the following syntax:
```
main.py [options]
```

Provided is a list of available options:
  - `--show-keys`, which prints the join and party key
  - `--show-rpc-dump`, which shows when the script dumps to `rpc.json`

### Troubleshooting
---

"Something went wrong while loading the configuration":
  - Make sure that `config.py` exists and is a valid Python file and is importable.
  - Make sure there are no syntax errors
  - Make sure that the `Config` class exists and is callable.

"The secretLib used is not valid in the context required":
  - Make sure the `secretLib` in `config.py` does not require a length passed to it.
    - This means that `shake` algorithms cannot be used as `secretLib`.
  - Make sure that `secretLib` is not set to `None`.

"secretLib needs to be set in order to use this":
  - Make sure that `secretLib` is not set to `None`.

"updateTime needs to be at least a 15 second interval":
  - Set `updateTime` to a value bigger than (or equal to) 15 (the required RPC delay).
