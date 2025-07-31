from math import pi, sin, cos
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLE_STRIP
from OpenGL.GL import *
from OpenGL.raw.GL.VERSION.GL_1_1 import glDrawArrays
import numpy

class SpherePrimative:
    """
    SpherePrimative creates and binds the OpenGL buffers needed to draw object into the scene
    """
    def __init__(self, stacks = 12, slices = 12):
        self.slices = slices
        self.vertex_count = 0

        vertex_array = []

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                for _ in range(2):
                    vertex_array.append( sin(stack_angle) * cos(slice_angle) )
                    vertex_array.append( cos(stack_angle) )
                    vertex_array.append( sin(stack_angle) * sin(slice_angle) )

                for _ in range(2):
                    vertex_array.append( sin(stack_angle + stack_interval) * cos(slice_angle) )
                    vertex_array.append( cos(stack_angle + stack_interval) )
                    vertex_array.append( sin(stack_angle + stack_interval) * sin(slice_angle) )

                self.vertex_count += 2
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader):
        """
        draw() sets the buffers in the shader file and draws the sphere

        @param 'shader' - The shader program to use
        """
        shader.set_attribute_buffers(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)