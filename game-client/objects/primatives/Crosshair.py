
from math import pi, cos, sin
from OpenGL.GL import *

class Crosshair:
    """
        Simple crosshair dot that stays in the center of the screen,
        color is set in the shader provided, and uses alpha channel to make
        the dot slightly transparent
    """
    def __init__(self, shader):
        """
        @param 'shader' - The shader program
        """
        self.samples = 21
        self.position_array = [0, 0]
        self.shader = shader

        rad = 0.005
        for i in range(0, self.samples):
            x = rad * cos(i * 2*pi / (self.samples - 1))
            y = rad * 1.8 * sin(i * 2*pi / (self.samples - 1))
            self.position_array.append(x)
            self.position_array.append(y)

    def draw(self):
        """
            Draws the crosshair using OpenGL calls
        """
        self.shader.use()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Really tried to make this work with shader files but I kept getting very unexpected results
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.0, 0.0)
        for i in range(0, self.samples*2+1, 2):
            glVertex2f(self.position_array[i], self.position_array[i+1])
        glEnd()
        glDisable(GL_BLEND)