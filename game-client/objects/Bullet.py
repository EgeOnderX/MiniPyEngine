import shortuuid

from maths.Point import Point
from maths.Color import Color
from maths.Vector import Vector
from maths.Material import Material
from .GameObjectBase import GameObject
from objects.primatives.SpherePrimative import SpherePrimative

class Bullet(GameObject):
    def __init__(self, shader, position=Point(1, 1, 1), direction=Vector(1, 0, 0), network_test=False):
        bullet_material = Material(Color(1, 0, 0), Color(1, 0, 0), 1)
        super().__init__(shader, position, Vector(0,0,0), Vector(0.02, 0.02, 0.02), bullet_material)
        self.direction = direction
        
        self.speed = 10
        if not network_test:
            self.sphere = SpherePrimative()
        self.collision_resize = 1
        self.network_uid = shortuuid.uuid()
    
    def update(self, delta_time, game_objects):
        self.position += self.direction * delta_time * self.speed
        
        if self.position.y <= -1 or self.position.y >= 15:
            self.destroy = True
        if abs(self.position.x) >= 15 or abs(self.position.z) >= 15:
            self.destroy = True
        
        collision_objects = game_objects.check_collision(self)
        
        for obj in collision_objects:
            if type(obj) != Bullet:
                self.destroy = True

    def draw(self, modelMatrix):
        self._draw(modelMatrix, self.sphere)
    
    def to_dict(self):
        bullet_dict = {
            'uid': self.network_uid,
            'data': {
                'direction':
                {
                    'x': self.direction.x,
                    'y': self.direction.y,
                    'z': self.direction.z
                },
                'position':
                {
                    'x': self.position.x,
                    'y': self.position.y,
                    'z': self.position.z
                }
            }
        }
        return bullet_dict
