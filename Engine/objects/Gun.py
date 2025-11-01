from maths.Vector import Vector
from maths.Point import Point
from maths.Color import Color
from maths.Material import Material
from objects.GameObjectBase import GameObject
from objects.TexturedCube import TexturedCube
import os, sys


class Gun(GameObject):
    """
    Basit silah objesi (şimdilik TexturedCube tabanlı)
    """

    def __init__(self, shader, position=Point(0, 0, 0), rotation=Vector(0, 0, 0),
                 scale=Vector(1, 1, 1), texture_path="textures/gun.png"):
        super().__init__(shader, position, rotation, scale, Material())
        self.shader = shader
        self.texture_path = os.path.join(sys.path[0], texture_path)
        self.visible = True

        # Küp oluştur
        self.cube = TexturedCube(shader, position, rotation, scale, texture_path=self.texture_path)

        # Silah alındı mı?
        self.picked_up = False

    def draw(self, modelMatrix):
        if self.visible and not self.picked_up:
            self.cube.draw(modelMatrix)

    def update(self, delta_time, game_objects):
        # Şimdilik hareket veya fizik yok
        pass

    def pick_up(self):
        self.picked_up = True
        self.visible = False