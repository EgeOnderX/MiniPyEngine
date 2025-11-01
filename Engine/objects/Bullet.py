from maths.Point import Point
from maths.Color import Color
from maths.Vector import Vector
from maths.Material import Material
from .GameObjectBase import GameObject
from objects.primatives.SpherePrimative import SpherePrimative

import pygame
import CONSTANTS

class Bullet(GameObject):
    def __init__(self, shader, position=Point(1, 1, 1), direction=Vector(1, 0, 0)):
        bullet_material = Material(Color(1, 0, 0), Color(1, 0, 0), 1)
        super().__init__(shader, position, Vector(0, 0, 0), Vector(0.01, 0.01, 0.01), bullet_material)
        
        self.direction = direction
        self.speed = CONSTANTS.BULLET_SPEED
        self.sphere = SpherePrimative()
        self.collision_resize = 1

        self.collided = False
        self.collision_time = 0

    def update(self, delta_time, game_objects):
        if self.collided:
            now = pygame.time.get_ticks()
            if now - self.collision_time >= CONSTANTS.BULLET_DESTROY_DELAY_MS:
                self.destroy = True
            return

        self.position += self.direction * delta_time * self.speed

        if self.position.y <= -1 or self.position.y >= CONSTANTS.BULLET_LIFETIME_BOUNDS:
            self.destroy = True
        if abs(self.position.x) >= CONSTANTS.BULLET_LIFETIME_BOUNDS or abs(self.position.z) >= CONSTANTS.BULLET_LIFETIME_BOUNDS:
            self.destroy = True

        collision_objects = game_objects.check_collision(self)
        for obj in collision_objects:
            if not isinstance(obj, Bullet):
                self.collided = True
                self.collision_time = pygame.time.get_ticks()

    def draw(self, modelMatrix):
        self._draw(modelMatrix, self.sphere)
