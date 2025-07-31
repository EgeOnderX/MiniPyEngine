import os
import sys
import importlib

class chk:
    @staticmethod
    def module():
        print("=== MiniPyEngine Module Checker ===")

        # Minimum Python version check
        min_version = (3, 10)
        current_version = sys.version_info[:3]
        if current_version >= min_version:
            print(f"[OK] Python {current_version[0]}.{current_version[1]} is installed (Required: >= 3.10)")
        else:
            print(f"[ERROR] Python {current_version[0]}.{current_version[1]} is too old! (Required: >= 3.10)")

        # List of required modules
        modules = [
            "OpenGL",      # PyOpenGL
            "psutil",
            "pygame",
            "os",
            "maths",       # Custom module
            "subprocess",
            "threading",
            "numpy"
        ]

        # Module availability check
        for mod in modules:
            try:
                importlib.import_module(mod)
                print(f"[OK] Module '{mod}' is installed.")
            except ImportError:
                print(f"[ERROR] Module '{mod}' is NOT installed!")

# Usage:
# chk.module()
