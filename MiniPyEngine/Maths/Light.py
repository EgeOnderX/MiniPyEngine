from OpenGL.GL import *

class Light:
    def __init__(self, position=(5.0, 10.0, 5.0, 1.0)):
        self.position = position
        self.ambient = (0.3, 0.3, 0.3, 1.0)
        self.diffuse = (0.8, 0.8, 0.8, 1.0)

    def apply(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_MATERIAL, GL_AMBIENT_AND_DIFFUSE)

        glLightfv(GL_LIGHT0, GL_POSITION, self.position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
