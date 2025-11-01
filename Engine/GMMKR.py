import os
import sys
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox

# === Paths ===
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
OBJECTS_DIR = os.path.join(PROJECT_DIR, "objects")

# Make sure Python sees "objects" as a package
if OBJECTS_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# === Load level1 dynamically ===
def load_level1():
    try:
        # Import as a package module: objects.level1
        if "objects.level1" in sys.modules:
            del sys.modules["objects.level1"]
        level_module = importlib.import_module("objects.level1")

        Level1 = getattr(level_module, "Level1", None)
        if Level1 is None:
            messagebox.showerror("Error", "Class 'Level1' not found in level1.py!")
            return None

        instance = Level1(shader=None, position=None)
        return instance

    except Exception as e:
        messagebox.showerror("Import Error", f"Error while loading Level1:\n{e}")
        return None


# === Extract object names from Level1 instance ===
def get_level_objects(level_instance):
    if not level_instance:
        return []
    return [
        attr for attr in vars(level_instance)
        if not attr.startswith("__") and attr != "cubes"
    ]


# === List other .py files in objects folder ===
def list_objects_dir():
    files = []
    for f in os.listdir(OBJECTS_DIR):
        if f.endswith(".py") and f not in ("__init__.py", "level1.py"):
            files.append(f)
    return files


# === Tkinter UI ===
class GMMKRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GMMKR - MiniPyEngine Game Maker")
        self.geometry("700x450")
        self.configure(bg="#1e1e1e")

        title = tk.Label(self, text="MiniPyEngine Game Maker", font=("Segoe UI", 14, "bold"),
                         fg="white", bg="#1e1e1e")
        title.pack(pady=10)

        container = tk.Frame(self, bg="#1e1e1e")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel
        left_frame = tk.Frame(container, bg="#2d2d2d", width=220)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        lbl1 = tk.Label(left_frame, text="Objects folder", fg="white", bg="#2d2d2d",
                        font=("Segoe UI", 10, "bold"))
        lbl1.pack(anchor="w", padx=10, pady=5)

        self.objects_list = tk.Listbox(left_frame, bg="#333", fg="white",
                                       selectbackground="#007acc", relief="flat")
        self.objects_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Right panel
        right_frame = tk.Frame(container, bg="#252526")
        right_frame.pack(side="right", fill="both", expand=True)

        lbl2 = tk.Label(right_frame, text="Objects inside Level1", fg="white", bg="#252526",
                        font=("Segoe UI", 10, "bold"))
        lbl2.pack(anchor="w", padx=10, pady=5)

        self.tree = ttk.Treeview(right_frame)
        self.tree["columns"] = ("type",)
        self.tree.heading("#0", text="Variable")
        self.tree.heading("type", text="Type")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Refresh button
        btn_refresh = tk.Button(self, text="Refresh", bg="#007acc", fg="white",
                                font=("Segoe UI", 10, "bold"), command=self.refresh_all)
        btn_refresh.pack(pady=5)

        self.refresh_all()

    def refresh_all(self):
        self.objects_list.delete(0, tk.END)
        for obj in list_objects_dir():
            self.objects_list.insert(tk.END, obj)

        for i in self.tree.get_children():
            self.tree.delete(i)

        level_instance = load_level1()
        if level_instance:
            objs = get_level_objects(level_instance)
            for name in objs:
                val = getattr(level_instance, name)
                typename = type(val).__name__
                self.tree.insert("", "end", text=name, values=(typename,))


# === Run ===
if __name__ == "__main__":
    app = GMMKRApp()
    app.mainloop()
