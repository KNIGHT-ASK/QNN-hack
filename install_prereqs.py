#!/usr/bin/env python3
"""
install_prereqs.py
Usage:
    python install_prereqs.py
Run this script to ensure all necessary dependencies are installed before executing your main file.
"""
import sys
import subprocess
import shutil

def printc(msg, color):
    colors = {'r': '\033[31m', 'g': '\033[32m', 'y': '\033[33m', '': ''}
    end = '\033[0m'
    print(f"{colors.get(color, '')}{msg}{end}")

def _ensure_packages():
    import importlib
    pkgs = [
        ("torch", "torch"),
        ("torchvision", "torchvision"),
        ("matplotlib", "matplotlib"),
        ("numpy", "numpy"),
    ]
    missing = []
    for mod_name, pip_name in pkgs:
        try:
            importlib.import_module(mod_name)
        except ImportError:
            missing.append(pip_name)
    # Special handling for numpy: try conda first
    if "numpy" in missing:
        printc("'numpy' not found. Attempting to install with conda...", 'y')
        if shutil.which('conda') is not None:
            conda_proc = subprocess.run(["conda", "install", "-y", "numpy"])
            if conda_proc.returncode == 0:
                printc("'numpy' installed with conda. You may now run your main script.", 'g')
                missing.remove("numpy")
            else:
                printc("Conda install failed or numpy not found in environment. Trying pip...", 'r')
        else:
            printc("'conda' is not available. Will try pip for 'numpy'.", 'y')
    # Now, check for anything still missing
    missing = []
    for mod_name, pip_name in pkgs:
        try:
            importlib.import_module(mod_name)
        except ImportError:
            missing.append(pip_name)
    if missing:
        printc("Missing: " + ', '.join(missing), 'r')
        print("Attempting to install missing dependencies with pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            printc("Install succeeded! You may now run your main script.", 'g')
        except subprocess.CalledProcessError as e:
            printc("ERROR: Automatic pip install failed.", 'r')
            print("You may need to install the following manually:")
            printc("    pip install " + ' '.join(missing), 'r')
            print(f"Details: {e}")
            sys.exit(1)
    else:
        printc("All dependencies already satisfied. You are set!", 'g')
    # Final check
    try:
        for mod_name, _ in pkgs:
            importlib.import_module(mod_name)
    except ImportError as e:
        printc("ERROR: Some dependencies could not be loaded after install. Try closing the terminal and starting a new one, or check your environment.", 'r')
        print(f"Details: {e}")
        sys.exit(1)

if __name__ == '__main__':
    _ensure_packages()
