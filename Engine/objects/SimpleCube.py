from OpenGL.GL import *
from objects.GameObjectBase import GameObject
from objects.primatives.CubePrimative import CubePrimative

class SimpleCube(GameObject):
    """
        A single cube gameobject that has collision
    """
    def __init__(self, shader, position, rotation, scale, material, visible=True):
        super().__init__(shader, position, rotation, scale, material, visible)
        
        self.cube = CubePrimative(has_uv=False)
        # x left, x right, z left, z right
        self.moving = [False, False, False, False]
    
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

    def draw(self, modelMatrix) -> None:
        self._draw(modelMatrix, self.cube)

    def update(self, delta_time, game_objects):
        pass