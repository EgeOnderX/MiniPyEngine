from OpenGL.GL import *

import sys

class ShaderCrosshair:
    def __init__(self):
        frag_shader = self.compile_shader(GL_FRAGMENT_SHADER, "crosshair.frag")

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

    def compile_shader(self, SHADER_TYPE, file_name):
        shader = glCreateShader(SHADER_TYPE)
        shader_file = open(sys.path[0] + "\\shaders\\" + file_name)
        glShaderSource(shader, shader_file.read())
        shader_file.close()
        glCompileShader(shader)
        result = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if (result != 1):
            print("Couldn't compile shader\nShader compilation log:\n" + str(glGetShaderInfoLog(shader)))
        else:
            print("Compiled shader " + shader_file.name)
        return shader
    
    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise