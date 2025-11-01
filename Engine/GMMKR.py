import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# === PATHS ===
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
MAPS_DIR = os.path.join(PROJECT_DIR, "maps")
OBJECTS_DIR = os.path.join(PROJECT_DIR, "objects")

if not os.path.exists(MAPS_DIR):
    os.makedirs(MAPS_DIR)

# === Utility functions ===
def list_maps():
    """List all .mpf files inside maps/"""
    return [f for f in os.listdir(MAPS_DIR) if f.endswith(".mpf")]

def load_mpf(path):
    """Read objects from .mpf file"""
    objs = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("object:"):
                    objs.append(line)
        return objs
    except Exception as e:
        messagebox.showerror("Load Error", str(e))
        return []

def append_to_mpf(path, obj_line):
    """Append new object line to map file"""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(obj_line + "\n")
    except Exception as e:
        messagebox.showerror("Write Error", str(e))

def parse_object_line(line):
    """Extract type and position from object line"""
    try:
        parts = line.split(",")
        obj_type = line.split(":")[1].split(",")[0].strip()
        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
        return obj_type, x, y, z
    except Exception:
        return "Unknown", 0, 0, 0

# === MAIN APP ===
class GMMKRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniPyEngine GMMKR")
        self.geometry("900x600")
        self.configure(bg="#1e1e1e")

        self.selected_map = None
        self.objects = []

        self.create_ui()
        self.select_map_dialog()

    # --- UI ---
    def create_ui(self):
        title = tk.Label(self, text="MiniPyEngine Map Maker", font=("Segoe UI", 14, "bold"),
                         fg="white", bg="#1e1e1e")
        title.pack(pady=10)

        container = tk.Frame(self, bg="#1e1e1e")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT PANEL - Object Templates
        left = tk.Frame(container, bg="#2d2d2d", width=220)
        left.pack(side="left", fill="y", padx=(0, 10))

        lbl_left = tk.Label(left, text="Object Templates", fg="white", bg="#2d2d2d",
                            font=("Segoe UI", 10, "bold"))
        lbl_left.pack(anchor="w", padx=10, pady=5)

        self.template_list = tk.Listbox(left, bg="#333", fg="white",
                                        selectbackground="#007acc", relief="flat")
        for item in ["Crate", "TexturedCube", "Gun", "Floor"]:
            self.template_list.insert(tk.END, item)
        self.template_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        tk.Button(left, text="Add to Map", bg="#007acc", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self.add_object).pack(pady=5)

        # RIGHT PANEL - Objects in Map
        right = tk.Frame(container, bg="#252526")
        right.pack(side="right", fill="both", expand=True)

        lbl_right = tk.Label(right, text="Objects in Map", fg="white", bg="#252526",
                             font=("Segoe UI", 10, "bold"))
        lbl_right.pack(anchor="w", padx=10, pady=5)

        self.tree = ttk.Treeview(right)
        self.tree["columns"] = ("type", "x", "y", "z")
        self.tree.heading("#0", text="Object Line")
        self.tree.heading("type", text="Type")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.heading("z", text="Z")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Mini map canvas (bottom)
        self.canvas = tk.Canvas(self, bg="#0f0f0f", height=180)
        self.canvas.pack(fill="x", padx=10, pady=10)

        # Buttons
        tk.Button(self, text="Refresh", bg="#007acc", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self.refresh).pack(pady=5)

    # --- Map Selection Dialog ---
    def select_map_dialog(self):
        maps = list_maps()
        if not maps:
            messagebox.showinfo("No Maps", "No .mpf files found in maps/ folder!")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Select Map File")
        dialog.geometry("300x250")
        dialog.configure(bg="#1e1e1e")

        tk.Label(dialog, text="Select a Map File:", bg="#1e1e1e", fg="white").pack(pady=10)

        listbox = tk.Listbox(dialog, bg="#2d2d2d", fg="white", selectbackground="#007acc")
        for m in maps:
            listbox.insert(tk.END, m)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        def select():
            sel = listbox.curselection()
            if sel:
                self.selected_map = os.path.join(MAPS_DIR, listbox.get(sel[0]))
                dialog.destroy()
                self.refresh()
            else:
                messagebox.showwarning("Select", "Please select a map file.")

        tk.Button(dialog, text="Load", command=select, bg="#007acc", fg="white").pack(pady=5)

    # --- Load objects ---
    def refresh(self):
        if not self.selected_map:
            return
        self.objects = load_mpf(self.selected_map)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for obj_line in self.objects:
            obj_type, x, y, z = parse_object_line(obj_line)
            self.tree.insert("", "end", text=obj_line, values=(obj_type, x, y, z))
        self.draw_minimap()

    # --- Mini Map ---
    def draw_minimap(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w // 2, h // 2
        scale = 10  # scaling factor for visualization

        for obj_line in self.objects:
            obj_type, x, y, z = parse_object_line(obj_line)
            px, py = cx + x * scale, cy + z * scale
            color = "lime" if obj_type.lower() == "crate" else "orange"
            self.canvas.create_rectangle(px - 4, py - 4, px + 4, py + 4, fill=color)

        self.canvas.create_line(cx, 0, cx, h, fill="#444")
        self.canvas.create_line(0, cy, w, cy, fill="#444")

    # --- Add Object ---
    def add_object(self):
        if not self.selected_map:
            messagebox.showwarning("No Map", "Select a map first!")
            return

        selected = self.template_list.curselection()
        if not selected:
            messagebox.showwarning("No Object", "Select an object type first!")
            return

        obj_type = self.template_list.get(selected[0])

        # Ask for transform data
        try:
            x = float(simpledialog.askstring("Position", "X position:", parent=self))
            y = float(simpledialog.askstring("Position", "Y position:", parent=self))
            z = float(simpledialog.askstring("Position", "Z position:", parent=self))
            sx = float(simpledialog.askstring("Scale", "Scale X:", parent=self))
            sy = float(simpledialog.askstring("Scale", "Scale Y:", parent=self))
            sz = float(simpledialog.askstring("Scale", "Scale Z:", parent=self))
        except Exception:
            messagebox.showerror("Invalid", "Invalid input values.")
            return

        obj_line = f"object: {obj_type}, {x},{y},{z}, 0,0,0, {sx},{sy},{sz}"
        append_to_mpf(self.selected_map, obj_line)
        self.refresh()


# === RUN ===
if __name__ == "__main__":
    app = GMMKRApp()
    app.mainloop()
