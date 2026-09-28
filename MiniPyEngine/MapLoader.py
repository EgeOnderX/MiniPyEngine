import os
import pygame
from OpenGL.GL import *

# === TEXTURE LOADER HELPER (WITH CACHING) ===
TEXTURE_CACHE = {}

def load_texture(texture_path):
    if not texture_path or not os.path.exists(texture_path):
        return 0

    abs_path = os.path.abspath(texture_path)
    # Doku daha önce yüklendiyse direkt VRAM'deki ID'yi döndür
    if abs_path in TEXTURE_CACHE:
        return TEXTURE_CACHE[abs_path]

    try:
        surface = pygame.image.load(texture_path)
        surface = surface.convert_alpha() if surface.get_alpha() else surface.convert()
        
        if hasattr(pygame.image, "tobytes"):
            image_data = pygame.image.tobytes(surface, "RGBA", True)
        else:
            image_data = pygame.image.tostring(surface, "RGBA", True)

        width, height = surface.get_width(), surface.get_height()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        TEXTURE_CACHE[abs_path] = texture_id
        return texture_id
    except Exception as e:
        print(f"[ERROR] MapLoader: Failed to load texture '{texture_path}': {e}")
        return 0


# === LOW-LEVEL OBJ / MTL LOADER ===
class OBJModel:
    def __init__(self, filename, fallback_texture=None):
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.materials = {}
        self.gl_list = None
        self.fallback_texture_id = load_texture(fallback_texture) if fallback_texture else 0

        if os.path.exists(filename):
            self.load_obj(filename)
            self.compile_display_list()
        else:
            print(f"[WARNING] OBJModel: File '{filename}' not found!")

    def load_obj(self, filename):
        dir_path = os.path.dirname(filename)
        current_material = None

        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                parts = line.split()
                if not parts:
                    continue

                if parts[0] == 'mtllib':
                    mtl_path = os.path.join(dir_path, parts[1])
                    self.load_mtl(mtl_path)
                elif parts[0] == 'v':
                    self.vertices.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'vt':
                    self.texcoords.append([float(x) for x in parts[1:3]])
                elif parts[0] == 'vn':
                    self.normals.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'usemtl':
                    current_material = parts[1]
                elif parts[0] == 'f':
                    face = []
                    for v in parts[1:]:
                        w = v.split('/')
                        v_idx = int(w[0]) - 1
                        vt_idx = int(w[1]) - 1 if len(w) > 1 and w[1] != '' else None
                        vn_idx = int(w[2]) - 1 if len(w) > 2 and w[2] != '' else None
                        face.append((v_idx, vt_idx, vn_idx))
                    self.faces.append((face, current_material))

    def load_mtl(self, filename):
        if not os.path.exists(filename):
            return
        
        dir_path = os.path.dirname(filename)
        mat_name = None

        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'newmtl':
                    mat_name = parts[1]
                    self.materials[mat_name] = {'texture': 0, 'kd': (1.0, 1.0, 1.0)}
                elif mat_name and parts[0] == 'map_Kd':
                    tex_file = os.path.join(dir_path, parts[1])
                    self.materials[mat_name]['texture'] = load_texture(tex_file)
                elif mat_name and parts[0] == 'Kd':
                    self.materials[mat_name]['kd'] = (float(parts[1]), float(parts[2]), float(parts[3]))

    def compile_display_list(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        
        # Yüzeyleri materyallerine göre grupla (State Switch'leri engeller)
        mat_groups = {}
        for face, mat_name in self.faces:
            if mat_name not in mat_groups:
                mat_groups[mat_name] = []
            mat_groups[mat_name].append(face)

        for mat_name, faces in mat_groups.items():
            mat = self.materials.get(mat_name, None)
            tex_id = mat['texture'] if mat and mat['texture'] != 0 else self.fallback_texture_id
            
            if tex_id != 0:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, tex_id)
            else:
                glDisable(GL_TEXTURE_2D)

            if mat:
                glColor3f(*mat['kd'])
            else:
                glColor3f(1.0, 1.0, 1.0)

            # GL_POLYGON YERİNE BATCHED GL_TRIANGLES (FPS Darboğazını Çözen Yer)
            glBegin(GL_TRIANGLES)
            for face in faces:
                # Poligonları/Dörtgenleri üçgenlere böl (Triangulation)
                for i in range(1, len(face) - 1):
                    triangle = [face[0], face[i], face[i+1]]
                    for v_idx, vt_idx, vn_idx in triangle:
                        if vn_idx is not None and vn_idx < len(self.normals):
                            glNormal3fv(self.normals[vn_idx])
                        if vt_idx is not None and vt_idx < len(self.texcoords) and tex_id != 0:
                            glTexCoord2fv(self.texcoords[vt_idx])
                        glVertex3fv(self.vertices[v_idx])
            glEnd()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()

    def draw(self):
        if self.gl_list:
            glCallList(self.gl_list)


# === MAP LOADER CLASS ===
class MapLoader:
    def __init__(self):
        from Objects.TexturedCube.TexturedCube import TexturedCube
        from Objects.Crate.Crate import Crate
        from Objects.Ammo.Ammo import Ammo
        from Objects.Gun.Gun import Gun
        from Objects.Floor.Floor import Floor
        from Objects.Walls.Walls import Walls
        from Objects.Cube.cube import Cube

        self.registry = {
            "TexturedCube": TexturedCube,
            "Crate": Crate,
            "Ammo": Ammo,
            "Gun": Gun,
            "Floor": Floor,
            "Walls": Walls,
            "Cube": Cube
        }

    def load_map(self, map_path):
        scene_objects = []
        
        if not os.path.exists(map_path):
            print(f"[ERROR] MapLoader: Map file '{map_path}' not found!")
            return scene_objects

        print(f"[INFO] MapLoader: Loading '{map_path}'...")
        
        with open(map_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('object:'):
                    raw_data = line.replace('object:', '').strip()
                    parts = [p.strip() for p in raw_data.split(',')]

                    if len(parts) < 10:
                        continue

                    obj_type = parts[0]
                    pos = (float(parts[1]), float(parts[2]), float(parts[3]))
                    rot = (float(parts[4]), float(parts[5]), float(parts[6]))
                    scale = (float(parts[7]), float(parts[8]), float(parts[9]))
                    tex = parts[10] if len(parts) > 10 else None

                    if obj_type in self.registry:
                        obj_instance = self.registry[obj_type](
                            position=pos,
                            rotation=rot,
                            scale=scale,
                            texture_path=tex
                        )
                        scene_objects.append(obj_instance)

        print(f"[INFO] MapLoader: Loaded {len(scene_objects)} objects.")
        return scene_objects
