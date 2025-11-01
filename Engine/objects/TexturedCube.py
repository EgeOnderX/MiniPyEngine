import sys
import pygame
from OpenGL.GL import *

from maths.Color import Color
from maths.Material import Material
from maths.Matricies import ModelMatrix
from objects.GameObjectBase import GameObject
from objects.primatives.CubePrimative import CubePrimative

class TexturedCube(GameObject):
    """
        A cube that has image textururing on it
    """
    def __init__(self, shader, position, rotation, scale, material=Material(Color(1, 1, 1), Color(.05, .05, .05), 250), visible=True, texture_path=None):
        super().__init__(shader, position, rotation, scale, material, visible)
        self.cube = CubePrimative()
        # x left, x right, z left, z right
        self.moving = [False, False, False, False]

        self.apply_texture = sys.path[0] + "\\textures\\missing.png"
        if texture_path != None:
            self.apply_texture = texture_path
        self.texture_id = self.load_texture(self.apply_texture)
    
    def load_texture(self, path):
        image = pygame.image.load(path)
        tex_string = pygame.image.tostring(image, "RGBA", 1)
        img_width = image.get_width()
        img_height = image.get_height()
        # Start opengl operations
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        # Generate a mipmap for the texture
        glGenerateMipmap(GL_TEXTURE_2D)
        return tex_id

    def move(self, change):
        # Change cube position by change
        if self.moving[0]:
            self.x -= change
        if self.moving[1]:
            self.x += change
        if self.moving[2]:
            self.z += change
        if self.moving[3]:
            self.z -= change

    def draw(self, modelMatrix : ModelMatrix) -> None:
        # Implement the draw call
        if self.visible:
            modelMatrix.load_identity()
            modelMatrix.push_matrix()

            modelMatrix.add_translation(self.position.x, self.position.y, self.position.z)
            modelMatrix.add_rotate_x(self.rotation.x)
            modelMatrix.add_rotate_y(self.rotation.y)
            modelMatrix.add_rotate_z(self.rotation.z)
            modelMatrix.add_scale(self.scale.x, self.scale.y, self.scale.z)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            self.shader.set_model_matrix(modelMatrix.matrix)
            self.shader.set_material_diffuse(self.material.diffuse)
            self.shader.set_material_specular(self.material.specular)
            self.shader.set_material_shininess(self.material.shininess)
            
            self.cube.draw(self.shader)
            modelMatrix.pop_matrix()

            glBindTexture(GL_TEXTURE_2D, 0)

    def update(self, delta_time, game_objects):
        pass