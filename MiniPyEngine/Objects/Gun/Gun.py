import os
from OpenGL.GL import *
from MapLoader import OBJModel
from Objects.TexturedCube.TexturedCube import TexturedCube

class Gun:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), texture_path=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale

        base_dir = os.path.dirname(__file__)
        obj_path = os.path.join(base_dir, "Gun.obj")
        tex_path = texture_path if texture_path else os.path.join(base_dir, "Gun.png")

        if os.path.exists(obj_path):
            self.model = OBJModel(obj_path, fallback_texture=tex_path)
            self.fallback = None
        else:
            self.model = None
            self.fallback = TexturedCube(position, rotation, scale, tex_path)

    def draw(self):
        if self.model:
            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)
            glRotatef(self.rotation[1], 0, 1, 0)
            glRotatef(self.rotation[2], 0, 0, 1)
            glScalef(*self.scale)
            self.model.draw()
            glPopMatrix()
        elif self.fallback:
            self.fallback.draw()
