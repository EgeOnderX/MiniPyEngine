from maths.Point import Point
from maths.Color import Color
from maths.Vector import Vector
from maths.Material import Material
from .GameObjectBase import GameObject
from .meshes import ObjLoader
import os

class Crowbar(GameObject):
    def __init__(self, shader, position=Point(1,1,1)):
        crowbar_material = Material(Color(0.4, 0, 0), Color(0.2, 0.2, 0.2), 1)
        super().__init__(shader, position, Vector(0,0,0), Vector(1,1,1), crowbar_material)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = ObjLoader.load_obj_file("models", "crowbar.obj") 

        self.attack_range = 2.0
        self.cooldown = 0.4
        self.attack_timer = 0
        self.collision_resize = 1

    def update(self, delta_time, game_objects):
        if self.attack_timer > 0:
            self.attack_timer -= delta_time

    def attack(self, game_objects):
        if self.attack_timer > 0:
            return
        for obj in game_objects.check_collision(self):
            if obj is not self and hasattr(obj, "destroy"):
                distance = (obj.position - self.position).length()
                if distance <= self.attack_range:
                    obj.destroy = True
        self.attack_timer = self.cooldown

    def draw(self, modelMatrix):
        self._draw(modelMatrix, self.model)
