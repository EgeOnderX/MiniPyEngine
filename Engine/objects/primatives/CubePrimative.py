from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

class CubePrimative:
    """
    CubePrimative creates and binds the OpenGL buffers needed to draw object into the scene
    """
    def __init__(self, has_uv=True):
        """
        @param 'has_uv' - If the cube should have uv coordinates for texturing
        """
        self.has_uv = has_uv
        cube_array = [
            #position           normals             uv
            -0.5, -0.5, -0.5,   0.0, 0.0, -1.0,     0.0, 0.0,
            -0.5, 0.5, -0.5,    0.0, 0.0, -1.0,     0.0, 1.0,
            0.5, 0.5, -0.5,     0.0, 0.0, -1.0,     1.0, 1.0,
            0.5, -0.5, -0.5,    0.0, 0.0, -1.0,     1.0, 0.0,

            -0.5, -0.5, 0.5,    0.0, 0.0, 1.0,      0.0, 0.0,
            -0.5, 0.5, 0.5,     0.0, 0.0, 1.0,      0.0, 1.0,
            0.5, 0.5, 0.5,      0.0, 0.0, 1.0,      1.0, 1.0,
            0.5, -0.5, 0.5,     0.0, 0.0, 1.0,      1.0, 0.0,

            -0.5, -0.5, -0.5,   0.0, -1.0, 0.0,     0.0, 0.0,
            0.5, -0.5, -0.5,    0.0, -1.0, 0.0,     0.0, 1.0,
            0.5, -0.5, 0.5,     0.0, -1.0, 0.0,     1.0, 1.0,
            -0.5, -0.5, 0.5,    0.0, -1.0, 0.0,     1.0, 1.0,

            -0.5, 0.5, -0.5,    0.0, 1.0, 0.0,      0.0, 0.0,
            0.5, 0.5, -0.5,     0.0, 1.0, 0.0,      0.0, 1.0,
            0.5, 0.5, 0.5,      0.0, 1.0, 0.0,      1.0, 1.0,
            -0.5, 0.5, 0.5,     0.0, 1.0, 0.0,      1.0, 0.0,

            -0.5, -0.5, -0.5,   -1.0, 0.0, 0.0,     0.0, 0.0,
            -0.5, -0.5, 0.5,    -1.0, 0.0, 0.0,     0.0, 1.0,
            -0.5, 0.5, 0.5,     -1.0, 0.0, 0.0,     1.0, 1.0,
            -0.5, 0.5, -0.5,    -1.0, 0.0, 0.0,     1.0, 0.0,

            0.5, -0.5, -0.5,    1.0, 0.0, 0.0,      0.0, 0.0,
            0.5, -0.5, 0.5,     1.0, 0.0, 0.0,      0.0, 1.0,
            0.5, 0.5, 0.5,      1.0, 0.0, 0.0,      1.0, 1.0,
            0.5, 0.5, -0.5,     1.0, 0.0, 0.0,      1.0, 0.0
        ]

        if not has_uv:
            cube_array = [
                #position           normals
                -0.5, -0.5, -0.5,   0.0, 0.0, -1.0,
                -0.5, 0.5, -0.5,    0.0, 0.0, -1.0,
                0.5, 0.5, -0.5,     0.0, 0.0, -1.0,
                0.5, -0.5, -0.5,    0.0, 0.0, -1.0,

                -0.5, -0.5, 0.5,    0.0, 0.0, 1.0,
                -0.5, 0.5, 0.5,     0.0, 0.0, 1.0,
                0.5, 0.5, 0.5,      0.0, 0.0, 1.0,
                0.5, -0.5, 0.5,     0.0, 0.0, 1.0,

                -0.5, -0.5, -0.5,   0.0, -1.0, 0.0,
                0.5, -0.5, -0.5,    0.0, -1.0, 0.0,
                0.5, -0.5, 0.5,     0.0, -1.0, 0.0,
                -0.5, -0.5, 0.5,    0.0, -1.0, 0.0, 

                -0.5, 0.5, -0.5,    0.0, 1.0, 0.0,
                0.5, 0.5, -0.5,     0.0, 1.0, 0.0,
                0.5, 0.5, 0.5,      0.0, 1.0, 0.0,
                -0.5, 0.5, 0.5,     0.0, 1.0, 0.0,

                -0.5, -0.5, -0.5,   -1.0, 0.0, 0.0,
                -0.5, -0.5, 0.5,    -1.0, 0.0, 0.0,
                -0.5, 0.5, 0.5,     -1.0, 0.0, 0.0,
                -0.5, 0.5, -0.5,    -1.0, 0.0, 0.0,

                0.5, -0.5, -0.5,    1.0, 0.0, 0.0,
                0.5, -0.5, 0.5,     1.0, 0.0, 0.0,
                0.5, 0.5, 0.5,      1.0, 0.0, 0.0, 
                0.5, 0.5, -0.5,     1.0, 0.0, 0.0,
            ]
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(cube_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Draw fuction for a primitive cube object
    def draw(self, shader):
        """
        draw() sets the buffers in the shader file and draws the sphere

        @param 'shader' - The shader program to use
        """
        if self.has_uv:
            shader.set_attrib_buffers_tex(self.vertex_buffer_id)
        else:
            shader.set_attribute_buffers(self.vertex_buffer_id)

        for i in range(0, 6):
            glDrawArrays(GL_TRIANGLE_FAN, i * 4, 4)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
