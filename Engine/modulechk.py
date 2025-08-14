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
            print(f"[MiniPyEngine Runtime Error] Python {current_version[0]}.{current_version[1]} is too old! (Required: >= 3.10)")
            
            sys.exit(1)

        # List of required modules
        modules = [
            "OpenGL",      # PyOpenGL
            "psutil",
            "pygame",
            "numpy"
        ]

        # Module availability check
        missing_modules = []
        for mod in modules:
            try:
                importlib.import_module(mod)
                print(f"[OK] Module '{mod}' is installed.")
            except ImportError:
                print(f"[ERROR] Module '{mod}' is NOT installed!")
                missing_modules.append(mod)

        # If any module is missing, ask but always bypass if not closed
        if missing_modules:
            print(f"\n[MiniPyEngine Runtime Error] Cannot find needed libraries: {', '.join(missing_modules)}")
            input("Press ENTER or type anything to bypass and continue: ")
            print("[WARNING] Bypass mode enabled. Continuing without some modules...")

# Usage:
# chk.module()
