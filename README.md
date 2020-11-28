# Custom Presence
### a small RPC presence program designed for customizability
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
  `--show-keys`, which prints the join and party key
  `--hide-rpc-dump`, which hides the "RPC information dumped" message
