import sys
from typing import List

from .Bullet import Bullet
from maths.Vector import Vector
from objects.GameObjectBase import GameObject
from objects.GameObjects import GameObjects
from .meshes.ObjLoader import load_obj_file

class Enemy(GameObject):
    """
    Enemy class is another player connected through the networking
    """
    def __init__(self, shader, position, rotation, scale, material, visible=True) -> None:
        super().__init__(shader, position, rotation, scale, material, visible)
        self.collision_resize = 6

        obj_location = sys.path[0] + "\\models\\"
        filename = "bean.obj"
        self.owned_bullets : List[Bullet] = []
        self.model = load_obj_file(obj_location, filename)
        self.network_uid = None
    
    def add_to_owned_bullets(self, bullet_obj : Bullet, game_objects : GameObjects):
        """
        add_to_owned_bullets() will add a new and only new bullet, to the list of owned bullets.
        """
        bullet_exists = False
        for bullet in self.owned_bullets:
            if bullet.network_uid == bullet_obj.network_uid:
                if bullet.destroy == True:
                    self.remove_owned_bullet(bullet)
                bullet_exists = True
        if not bullet_exists:
            game_objects.add_object(bullet_obj)
            self.owned_bullets.append(bullet_obj)
    
    def remove_owned_bullet(self, bullet_obj : Bullet):
        self.owned_bullets.remove(bullet_obj)
    
    def update(self, delta_time, game_objects) -> None:
        pass
    
    def draw(self, modelMatrix) -> GameObject:
        self._draw(modelMatrix, self.model)