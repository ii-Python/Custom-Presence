# Modules
import platform
import subprocess

from shutil import which
from os import name, remove

# Requirements
requirements = {
    "nt": ["pywin32"],
    "global": ["psutil", "colorama", "pypresence"]
}
python_versions = ["python", "python3", "python3.7", "python3.8", "python3.9"]

# Install initialization
print("Custom Presence - Install Script")
print(f"This system is running {platform.system()}")

print()
print("Trying to detect Python installation...")

python = None
for ver in python_versions:
    if which(ver):
        python = ver
        print(f"  detected {ver}")

if python is None:
    python = input("Enter your python command: ")
    if not which(python):
        print("Invalid python command, consult the docs.")
        exit()

# Installer
def install_dep(dep):
    stdout = open("installer.log", "a")
    subprocess.run([python, "-m", "pip", "install", "--upgrade", dep], stdout = stdout)

print()
print("Trying to update pip...")
install_dep("pip")
print("  updated pip")

print()
print("Now installing requirements...")

for req in requirements["global"]:
    install_dep(req)
    print(f"  installed {req}")

# Install additional requirements
if name in requirements:
    extra_deps = requirements[name]
    print(f"  installing extra requirements for {name}...")

    for dep in extra_deps:
        install_dep(dep)
        print(f"    installed {dep}")

# Clean up our installer
try:
    remove("installer.log")
except PermissionError:
    pass

# Finished
print()
print("Install completed successfully!")
