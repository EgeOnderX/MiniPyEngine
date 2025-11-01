from OpenGL.GL import *
import OpenGL.GLU
from math import *

import sys

from maths.Color import Color


class Shader3D:
    def __init__(self):
        # Compiling and linking the shader files
        vert_shader = self.compile_shader(GL_VERTEX_SHADER, "simple3D.vert")
        frag_shader = self.compile_shader(GL_FRAGMENT_SHADER, "simple3D.frag")

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        # Getting the shader variable locations
        self.positionLoc    = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)
        self.normalLoc      = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)
        self.uvLoc          = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.eyePosLoc              = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        # self.lightPosLoc            = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDifLoc            = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecLoc           = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.lightAmbLoc            = glGetUniformLocation(self.renderingProgramID, "u_light_ambient")

        self.matDifLoc              = glGetUniformLocation(self.renderingProgramID, "u_material_diffuse")
        self.matSpecLoc             = glGetUniformLocation(self.renderingProgramID, "u_material_specular")
        self.matShinyLoc            = glGetUniformLocation(self.renderingProgramID, "u_material_shininess")
        self.diffuseTexLoc          = glGetUniformLocation(self.renderingProgramID, "u_tex01")

        self.modelMatrixLoc         = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc          = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc    = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.usingTextureLoc        = glGetUniformLocation(self.renderingProgramID, "u_is_texture")
    
    #
    # Returns the reference number of the shader file after compiling
    #
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
    
    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, a_normal):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, a_normal)
    
    def set_uv_attribute(self, uv):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, uv)

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)
    
    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)
    
    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos, i):
        get_position = glGetUniformLocation(self.renderingProgramID, f"u_light_position[{i}]")
        glUniform4f(get_position, pos.x, pos.y, pos.z, 1.0)
    
    def set_light_specular(self, color, i):
        get_position = glGetUniformLocation(self.renderingProgramID, f"lights[{i}].specular")
        glUniform4f(get_position, color.r, color.g, color.b, color.a)
    
    def set_light_diffuse(self, color, i):
        get_position = glGetUniformLocation(self.renderingProgramID, f"lights[{i}].diffuse")
        glUniform4f(get_position, color.r, color.g, color.b, color.a)
    
    def set_light_ambient(self, color, i):
        get_position = glGetUniformLocation(self.renderingProgramID, f"lights[{i}].ambient")
        glUniform4f(get_position, color.r, color.g, color.b, color.a)
    
    def set_material_diffuse(self, *args):
        if len(args) == 1 and isinstance(args[0], Color):
            color = args[0]
            glUniform4f(self.matDifLoc, color.r, color.g, color.b, 1.0)
        elif len(args) == 3:
            r, g, b = args[0], args[1], args[2]
            glUniform4f(self.matDifLoc, r, g, b, 1.0)
    
    def set_material_specular(self, *args):
        if len(args) == 1 and isinstance(args[0], Color):
            color = args[0]
            glUniform4f(self.matSpecLoc, color.r, color.g, color.b, 1.0)
        elif len(args) == 3:
            r, g, b = args[0], args[1], args[2]
            glUniform4f(self.matSpecLoc, r, g, b, 1.0)
    
    def set_material_shininess(self, shiny):
        glUniform1f(self.matShinyLoc, shiny)
    
    def set_diffuse_texture(self, tex):
        glUniform1f(self.diffuseTexLoc, tex)
    
    def set_attribute_buffers(self, vertex_buffer_id):
        glUniform1f(self.usingTextureLoc, 0.0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    def set_attrib_buffers_tex(self, vertex_buffer_id):
        glUniform1f(self.usingTextureLoc, 1.0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))
    
    """
    Texture testing
    """

    def set_specular_texture(self, specularTexture):
        pass
