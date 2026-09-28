import os
from OpenGL.GL import *
from Engine import GameObject, Vector3
from MapLoader import load_texture

class Floor(GameObject):
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), texture_path=None):
        super().__init__(position, rotation, scale)

        # Dokunun (Texture) yolunu belirleme
        base_dir = os.path.dirname(__file__)
        if not texture_path:
            texture_path = os.path.join(base_dir, "Floor.png")

        self.texture_path = texture_path
        self.texture_id = load_texture(self.texture_path)

    def draw(self):
        if not self.enabled:
            return

        glPushMatrix()
        
        # Engine.Transform üzerindeki dönüşümleri uygula
        self.transform.apply_transformations()

        # Kaplama bağlama ve kontrol işlemleri
        if self.texture_id != 0:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            glDisable(GL_TEXTURE_2D)

        glColor3f(1.0, 1.0, 1.0)

        # Zemin geometrisi ve normal vektörleri
        glBegin(GL_QUADS)
        
        # Üst Yüzey (Zemin Alanı)
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.0, -0.5)
        glTexCoord2f(10.0, 0.0); glVertex3f(0.5, 0.0, -0.5)
        glTexCoord2f(10.0, 10.0); glVertex3f(0.5, 0.0, 0.5)
        glTexCoord2f(0.0, 10.0); glVertex3f(-0.5, 0.0, 0.5)

        # Alt Yüzey
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.1, -0.5)
        glTexCoord2f(10.0, 0.0); glVertex3f(0.5, -0.1, -0.5)
        glTexCoord2f(10.0, 10.0); glVertex3f(0.5, -0.1, 0.5)
        glTexCoord2f(0.0, 10.0); glVertex3f(-0.5, -0.1, 0.5)

        glEnd()

        glEnable(GL_TEXTURE_2D)
        glPopMatrix()
