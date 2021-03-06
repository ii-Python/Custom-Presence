# Modules
import psutil
import subprocess

from ..utils.colors import colored
from ..utils.logging import info, verbose

try:
    import win32gui
    import win32process

except ImportError:

    info(colored("Failed to import pywin32, falling back to linux-based mechanism.", "yellow"))
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

    def app_running(self, name):

        for app in self.get_bg_apps():

            try:
                p = psutil.Process(app)
            except psutil.NoSuchProcess:
                continue

            if p.name().replace(".exe", "").lower() == name:
                return True

        return False

    def get_available_bg_apps(self):

        apps = []
        for a in self.get_bg_apps():

            try:
                p = psutil.Process(a)
            except psutil.NoSuchProcess:
                continue

            n = p.name().replace(".exe", "").lower()
            if n in self.rpc.config["applications"]:
                if self.app_running(n):
                    apps.append(p.pid)

        if not apps:
            apps = self.get_bg_apps()

        return apps

    def get_window_title(self, app):

        if app is not None:
            return win32gui.GetWindowText(app)

        # Linux method
        o = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            stdout = subprocess.PIPE
        ).stdout

        return o.decode("utf-8")

    def locate_app(self):

        win32app = None
        if win32gui is not None:

            # Windows method
            win32app = win32gui.GetForegroundWindow()
            verbose("Located app", win32app, "as the foreground window.")

            # For when a process is quickly closed or for the desktop sometimes
            pid = win32process.GetWindowThreadProcessId(win32app)[-1]

        else:

            # Linux/*nix systems
            out = subprocess.run(["xdotool", "getactivewindow", "getwindowpid"], stdout = subprocess.PIPE)
            pid = int(out.stdout.decode("utf-8"))

        # Check our PID is positive
        if pid < 0:
            return None  # Incredibly rare to reproduce

        # Turn our PID into a psutil process
        app = psutil.Process(pid)
        app = app.name()

        app = app.replace(".exe", "")  # windows
        app = app.lower()  # lowercase-only

        # Run through our weighted apps
        apps = self.rpc.config["applications"]
        weighted = {}
        for _ in apps:
            if apps[_]["weight"] > 0:
                if self.app_running(_):
                    weighted[_] = apps[_]["weight"]

        if weighted:
            app = max(weighted, key = len)

        # Chromium browsers
        if app in self.rpc.config["browsers"]:
            title = self.get_window_title(win32app)
            return title + "|CSPRC_CHROMIUM"

        # Check our app is available
        if app not in self.rpc.config["applications"]:
            return None

        return app
