
import sys
import pygame
from OpenGL.GL import *

from maths.Color import Color
from shaders.Shaders import Shader3D
from objects.GameObjectBase import GameObject
from objects.TexturedCube import CubePrimative


class Floor(GameObject):
    """
        The floor gameobject
    """
    def __init__(self, shader : Shader3D, position, rotation, scale, material, visible=True):
        material.specular = Color(80/255, 123/255, 231/255)
        material.diffuse = Color(80/255, 123/255, 231/255)
        material.shininess = 1
        super().__init__(shader, position, rotation, scale, material, visible)
        self.cube = CubePrimative()

        floor_texture = sys.path[0] + "\\textures\\metal_big_floor-min.png"
        self.texture_id = self.load_texture(floor_texture)
    
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

    def collision(self, n) -> None:
        # Skip collision checking
        return None

    def draw(self, modelMatrix) -> None:
        # Implement the draw call
        self.shader.use()
        modelMatrix.load_identity()
        modelMatrix.push_matrix()

        modelMatrix.add_translation(self.position.x, self.position.y, self.position.z)
        modelMatrix.add_scale(self.scale.x, self.scale.y, self.scale.z)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        self.shader.set_material_specular(80/255, 123/255, 231/255)
        self.shader.set_material_diffuse(80/255, 123/255, 231/255)
        self.shader.set_material_shininess(1)
        self.shader.set_model_matrix(modelMatrix.matrix)
        self.cube.draw(self.shader)
        modelMatrix.pop_matrix()
    
    def update(self, delta_time, game_objects):
        pass
