from __future__ import annotations
from sys import flags

from maths.Point import Point
from maths.Vector import Vector
from maths.Material import Material
from maths.Matricies import ModelMatrix
from shaders.Shaders import Shader3D

class GameObject:
    """
        'GameObject' is a base class that each game object should inherit from,
        it contains common functions and variables that each game object MUST have.

        It became incresingly more difficult to work with slightly different implementations of each game object's position, rotation, scale and others.
    """
    def __init__(self, shader : Shader3D, position : Point, rotation : Vector, scale : Vector, material : Material, visible=True) -> None:
        """
        @param 'shader' - The shader that will be used to communicate with GLSL shader files
        @param 'positon' - The position of the game object, expects Point
        @param 'rotation' - The rotation of the game object, expects Vector
        @param 'scale' - The scale of the game object, expects Vector
        @param 'material' - The material of the game object, expects Material
        @param 'visible' - Boolean if the object is visible or not (True by default)
        """
        if type(position) != Point:
            raise Exception("Incorrect type 'position' for GameObject, expected a Point")

        if type(rotation) != Vector:
            raise Exception("Incorrect type 'rotation' for GameObject, expected a Vector")
        
        if type(scale) != Vector:
            raise Exception("Incorrect type 'scale' for GameObject, expected a Vector")
        
        if type(material) != Material:
            raise Exception("Incorrect type 'material' for GameObject, expected a Material")
        
        if type(visible) != bool:
            raise Exception("Incorrect type 'visible' for GameObject, expected a boolean")

        self.shader = shader
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.material = material
        self.visible = visible

        self.collision_side = [0, 0, 0, 0]
        self.collision_resize = 2

        self.destroy = False
        self.disable_collision = False
    
    def collision(self, object : GameObject) -> GameObject:
        """
        Generic AABB collision for every game object, override this function if different collision is needed

        @param 'object' - the other game object that is being tested for collision
        """
        if not self.disable_collision:
            self.collision_side = [0, 0, 0, 0]
            p_x = object.position.x
            p_z = object.position.z

            x1 = self.position.x + (self.scale.x / self.collision_resize + 0.2)
            x2 = self.position.x - (self.scale.x / self.collision_resize + 0.2)

            z1 = self.position.z + (self.scale.z / self.collision_resize + 0.2)
            z2 = self.position.z - (self.scale.z / self.collision_resize + 0.2)

            if p_x <= x1 and p_x >= x2 and p_z <= z1 and p_z >= z2:
                x_h1 = abs(p_x - x1)
                x_h2 = abs(p_x - x2)
                z_h1 = abs(p_z - z1)
                z_h2 = abs(p_z - z2)

                if x_h1 < x_h2 and x_h1 < z_h1 and x_h1 < z_h2:
                    self.collision_side[0] = 1
                elif x_h2 < x_h1 and x_h2 < z_h1 and x_h2 < z_h2:
                    self.collision_side[1] = 1
                elif z_h1 < x_h1 and z_h1 < x_h2 and z_h1 < z_h2:
                    self.collision_side[2] = 1
                elif z_h2 < x_h1 and z_h2 < x_h2 and z_h2 < z_h1:
                    self.collision_side[3] = 1
                return self
            return None
    
    def _draw(self, modelMatrix : ModelMatrix, primative) -> GameObject:
        """
        Generic draw call that works for most objects, needs to be overwritten if textures are added

        @param 'modelMatrix' - the model matrix that will be used
        @param 'primative' - a primative object that uses OpenGL calls for drawing
        """
        if self.visible:
            modelMatrix.load_identity()
            modelMatrix.push_matrix()

            modelMatrix.add_translation(self.position.x, self.position.y, self.position.z)
            modelMatrix.add_rotate_x(self.rotation.x * 3.1415/180)
            modelMatrix.add_rotate_y(self.rotation.y * 3.1415/180)
            modelMatrix.add_rotate_z(self.rotation.z * 3.1415/180)
            modelMatrix.add_scale(self.scale.x, self.scale.y, self.scale.z)

            self.shader.use()
            self.shader.set_model_matrix(modelMatrix.matrix)
            self.shader.set_material_diffuse(self.material.diffuse)
            self.shader.set_material_specular(self.material.specular)
            self.shader.set_material_shininess(self.material.shininess)

            primative.draw(self.shader)
            modelMatrix.pop_matrix()
    
    def update(self, delta_time, game_objects) -> None:
        """
        update() can differ greatly between objects

        @param 'delta_time' - time difference between the previous and current frame
        @param 'game_objects' - the object that handles all of the game objects
        """
        return None
    
    def set_position(self, position):
        self.position = position