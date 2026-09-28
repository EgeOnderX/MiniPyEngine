from OpenGL.GL import *

class Cube:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), **kwargs):
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)

        glDisable(GL_TEXTURE_2D)
        glColor3f(0.7, 0.7, 0.7)

        glBegin(GL_QUADS)
        # Front
        glVertex3f(-0.5, -0.5,  0.5); glVertex3f( 0.5, -0.5,  0.5)
        glVertex3f( 0.5,  0.5,  0.5); glVertex3f(-0.5,  0.5,  0.5)
        # Back
        glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5,  0.5, -0.5)
        glVertex3f( 0.5,  0.5, -0.5); glVertex3f( 0.5, -0.5, -0.5)
        # Top
        glVertex3f(-0.5,  0.5, -0.5); glVertex3f(-0.5,  0.5,  0.5)
        glVertex3f( 0.5,  0.5,  0.5); glVertex3f( 0.5,  0.5, -0.5)
        # Bottom
        glVertex3f(-0.5, -0.5, -0.5); glVertex3f( 0.5, -0.5, -0.5)
        glVertex3f( 0.5, -0.5,  0.5); glVertex3f(-0.5, -0.5,  0.5)
        # Right
        glVertex3f( 0.5, -0.5, -0.5); glVertex3f( 0.5,  0.5, -0.5)
        glVertex3f( 0.5,  0.5,  0.5); glVertex3f( 0.5, -0.5,  0.5)
        # Left
        glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5, -0.5,  0.5)
        glVertex3f(-0.5,  0.5,  0.5); glVertex3f(-0.5,  0.5, -0.5)
        glEnd()

        glEnable(GL_TEXTURE_2D)
        glPopMatrix()
