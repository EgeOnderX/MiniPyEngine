from maths.Vector import Vector
from maths.Point import Point
from maths.Color import Color
from maths.Material import Material
from objects.GameObjectBase import GameObject
from objects.TexturedCube import TexturedCube
from .Crate import Crate
from .SimpleCube import SimpleCube
from .Gun import Gun
import sys, os


class Level1(GameObject):
    def __init__(self, shader, position=Point(0, 0, 0), rotation=Vector(0, 0, 0), scale=Vector(0, 0, 0), material=Material(), visible=True):
        super().__init__(shader, position, rotation, scale, material, visible)
        self.cubes = []
        self.destroy = False

        # --- 1. maps/default.mpf dosyasını bul ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(base_dir, "..", "maps", "default.mpf")
        map_path = os.path.normpath(map_path)

        if not os.path.exists(map_path):
            print(f"[ERROR] Map file not found: {map_path}")
            return

        print(f"[INFO] Loading map: {map_path}")

        # --- 2. Harita dosyasını satır satır oku ---
        with open(map_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("object:"):
                    # Format:
                    # object: Type, px,py,pz, rx,ry,rz, sx,sy,sz, [extra...]
                    parts = [p.strip() for p in line.split(",")]
                    obj_type = parts[0].split(":")[1].strip()

                    # Pozisyon, rotasyon, ölçek
                    pos = Point(float(parts[1]), float(parts[2]), float(parts[3]))
                    rot = Vector(float(parts[4]), float(parts[5]), float(parts[6]))
                    scl = Vector(float(parts[7]), float(parts[8]), float(parts[9]))

                    # --- Opsiyonel alanlar (texture / renk / parlaklık) ---
                    tex = None
                    color = None
                    shiny = 32.0

                    extras = parts[10:]
                    if extras:
                        # Eğer PNG ile bitiyorsa texture
                        if extras[0].endswith(".png"):
                            tex = extras[0]
                        # Renk varsa
                        elif len(extras) >= 4:
                            color = Color(float(extras[0]), float(extras[1]), float(extras[2]))
                            shiny = float(extras[3])

                    # --- Objeyi oluştur ---
                    obj = None
                    if obj_type == "TexturedCube":
                        if tex:
                            tex_path = os.path.join(sys.path[0], tex)
                            obj = TexturedCube(shader, pos, rot, scl, texture_path=tex_path)
                    elif obj_type == "SimpleCube":
                        mat = Material(color if color else Color(1, 1, 1),
                                       color if color else Color(1, 1, 1),
                                       shiny)
                        obj = SimpleCube(shader, pos, rot, scl, mat)
                    elif obj_type == "Crate":
                        obj = Crate(shader, pos, rot, scl)
                    elif obj_type == "Gun":
                        tex = extras[0] if extras else "textures/gun.png"
                        obj = Gun(shader, pos, rot, scl, texture_path=tex)

                    else:
                        print(f"[INFO] Unknown object type: {obj_type}")
                        continue

                    if obj:
                        self.cubes.append(obj)

        print(f"[INFO] Loaded {len(self.cubes)} objects from map.")

    def collision(self, obj) -> GameObject:
        collisions = []
        for cube in self.cubes:
            c = cube.collision(obj)
            if c:
                collisions.append(c)
        return collisions if collisions else None

    def draw(self, modelMatrix) -> None:
        for cube in self.cubes:
            cube.draw(modelMatrix)

    def update(self, delta_time, game_objects):
        pass
