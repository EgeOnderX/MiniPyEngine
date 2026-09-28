import os
from OpenGL.GL import *
from MapLoader import OBJModel
from Objects.TexturedCube.TexturedCube import TexturedCube

class Ammo:
    # Tüm Ammo objelerinin ortak kullanacağı tekil model ve hafıza referansları
    _shared_model = None
    _shared_fallback = None
    _is_initialized = False

    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), texture_path=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.active = True

        # Modeli hafızaya ve GPU'ya SADECE İLK AMMO OLUŞTUĞUNDA 1 DEFA yükle
        if not Ammo._is_initialized:
            base_dir = os.path.dirname(__file__)
            obj_path = os.path.join(base_dir, "Ammo.obj")
            tex_path = texture_path if texture_path else os.path.join(base_dir, "Ammo.jpg")

            if os.path.exists(obj_path):
                Ammo._shared_model = OBJModel(obj_path, fallback_texture=tex_path)
            else:
                Ammo._shared_fallback = TexturedCube((0,0,0), (0,0,0), (1,1,1), tex_path)
            
            Ammo._is_initialized = True

    def interact(self, player):
        if self.active:
            player.ammo += 30
            self.active = False
            print("[INFO] Ammo: Collected +30 bullets!")

    def draw(self):
        if not self.active:
            return

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)

        # Ayrı ayrı model nesneleri değil, ortak yüklenen modeli çiz
        if Ammo._shared_model:
            Ammo._shared_model.draw()
        elif Ammo._shared_fallback:
            Ammo._shared_fallback.draw()

        glPopMatrix()
