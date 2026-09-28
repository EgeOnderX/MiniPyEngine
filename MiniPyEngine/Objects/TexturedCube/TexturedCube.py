from OpenGL.GL import *
from MapLoader import load_texture

class TexturedCube:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), texture_path=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.texture_id = load_texture(texture_path)

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        # Front
        glTexCoord2f(0,0); glVertex3f(-0.5, -0.5,  0.5)
        glTexCoord2f(1,0); glVertex3f( 0.5, -0.5,  0.5)
        glTexCoord2f(1,1); glVertex3f( 0.5,  0.5,  0.5)
        glTexCoord2f(0,1); glVertex3f(-0.5,  0.5,  0.5)
        # Back
        glTexCoord2f(1,0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1,1); glVertex3f(-0.5,  0.5, -0.5)
        glTexCoord2f(0,1); glVertex3f( 0.5,  0.5, -0.5)
        glTexCoord2f(0,0); glVertex3f( 0.5, -0.5, -0.5)
        # Top
        glTexCoord2f(0,1); glVertex3f(-0.5,  0.5, -0.5)
        glTexCoord2f(0,0); glVertex3f(-0.5,  0.5,  0.5)
        glTexCoord2f(1,0); glVertex3f( 0.5,  0.5,  0.5)
        glTexCoord2f(1,1); glVertex3f( 0.5,  0.5, -0.5)
        # Bottom
        glTexCoord2f(1,1); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(0,1); glVertex3f( 0.5, -0.5, -0.5)
        glTexCoord2f(0,0); glVertex3f( 0.5, -0.5,  0.5)
        glTexCoord2f(1,0); glVertex3f(-0.5, -0.5,  0.5)
        # Right
        glTexCoord2f(1,0); glVertex3f( 0.5, -0.5, -0.5)
        glTexCoord2f(1,1); glVertex3f( 0.5,  0.5, -0.5)
        glTexCoord2f(0,1); glVertex3f( 0.5,  0.5,  0.5)
        glTexCoord2f(0,0); glVertex3f( 0.5, -0.5,  0.5)
        # Left
        glTexCoord2f(0,0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1,0); glVertex3f(-0.5, -0.5,  0.5)
        glTexCoord2f(1,1); glVertex3f(-0.5,  0.5,  0.5)
        glTexCoord2f(0,1); glVertex3f(-0.5,  0.5, -0.5)
        glEnd()

        glPopMatrix()
