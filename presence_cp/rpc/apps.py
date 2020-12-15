# Modules
import psutil
import random

from ..utils.colors import colored
from ..utils.logging import info, verbose

try:
    import win32gui
    import win32process

except:

    info(colored("Failed to import pywin32, falling back to old choice mechanism.", "yellow"))
    win32gui, win32process = None, None

# Main class
class ApplicationHandler(object):

    def __init__(self, rpc):
        self.rpc = rpc

    def get_bg_apps(self):

        running = []

        try:

            for program in psutil.process_iter():
                name = program.pid

                if name in running:
                    continue

                running.append(name)

        except KeyboardInterrupt:
            self.rpc.kill()  # Rare, but it happens

        return running

    def get_available_bg_apps(self):

        return self.get_bg_apps()

    def locate_app(self):

        if win32gui is not None:

            # Windows method
            app = win32gui.GetForegroundWindow()
            verbose("Located app", app, "as the foreground window.")

            # For when a process is quickly closed or for the desktop sometimes
            pid = win32process.GetWindowThreadProcessId(app)

        else:

            # Linux/*nix systems
            apps = self.get_available_bg_apps()
            pid = random.choice(apps)

        return pid
