from maths.Vector import Vector
from maths.Point import Point

import sys
from objects.GameObjectBase import GameObject

from .Crate import Crate
from maths.Color import Color
from .SimpleCube import SimpleCube
from maths.Material import Material
from objects.TexturedCube import TexturedCube

class Level1(GameObject):
    """
        The Level1 gameobject
    """
    def __init__(self, shader, position, rotation=Vector(0, 0, 0), scale=Vector(0, 0, 0), material=Material(), visible=True) -> None:
        super().__init__(shader, position, rotation, scale, material, visible)
        
        wall_color = (78/255, 233/255, 81/255)
        longwall = sys.path[0] + "\\textures\\longwall.png"
        longwallr = sys.path[0] + "\\textures\\longwall2.png"
        self.wall1 = TexturedCube(shader, Point(0, 0.2, 10), Vector(0, 0, 0), Vector(20, 1.5, 0.1), texture_path=longwall)
        self.wall2 = TexturedCube(shader, Point(0, 0.2, -10), Vector(0, 0, 0), Vector(20, 1.5, 0.1), texture_path=longwall)
        
        self.wall3 = TexturedCube(shader, Point(10, 0.2, 0), Vector(0, 0, 0), Vector(0.1, 1.5, 20), texture_path=longwallr)
        self.wall4 = TexturedCube(shader, Point(-10, 0.2, 0), Vector(0, 0, 0), Vector(0.1, 1.5, 20), texture_path=longwallr)
        
        obst_shiny = 25
        q1_diffuse = Color(244/255, 67/255, 54/255)
        q1_specular = Color(1.0, 67/255, 54/255)
        q1_mat = Material(q1_diffuse, q1_specular, obst_shiny)

        q2_diffuse = Color(76/255, 175/255, 80/255)
        q2_specular = Color(76/255, 1.0, 80/255)
        q2_mat = Material(q2_diffuse, q2_specular, obst_shiny)

        q3_diffuse = Color(33/255, 150/255, 243/255)
        q3_specular = Color(33/255, 150/255, 1.0)
        q3_mat = Material(q3_diffuse, q3_specular, obst_shiny)

        q4_diffuse = Color(1.0, 193/255, 7/255)
        q4_specular = Color(1.0, 193/255, 7/255)
        q4_mat = Material(q4_diffuse, q4_specular, obst_shiny)

        # Quadrant 1
        self.q1_cube_obsticle_1 = SimpleCube(shader, Point(6.5, 0.2, -8.5), Vector(0, 0, 0), Vector(1, 1.5, 3), q1_mat)
        self.q1_cube_obsticle_2 = SimpleCube(shader, Point(2.5, 0.2, -3.5), Vector(0, 0, 0), Vector(5, 1.5, 5), q1_mat)
        self.q1_cube_obsticle_3 = SimpleCube(shader, Point(8.5, 0.2, -2),   Vector(0, 0, 0), Vector(3, 1.5, 4), q1_mat)

        # Quadrant 2
        self.q2_cube_obsticle_1 = SimpleCube(shader, Point(-7, 0.2, -7, ), Vector(0, 0, 0), Vector(2.0, 1.5, 2.0), q2_mat)
        self.q2_cube_obsticle_2 = SimpleCube(shader, Point(-3, 0.2, -9, ), Vector(0, 0, 0), Vector(2.0, 1.5, 2.0), q2_mat)
        self.q2_cube_obsticle_3 = SimpleCube(shader, Point(-9, 0.2, -3, ), Vector(0, 0, 0), Vector(2.0, 1.5, 2.0), q2_mat)
        self.q2_cube_obsticle_4 = SimpleCube(shader, Point(-2, 0.2, -3.5), Vector(0, 0, 0), Vector(4, 1.5, 5),     q2_mat)

        # Quadrant 3
        self.q3_cube_obsticle_1 = SimpleCube(shader, Point(-8, 0.2, 6.5),   Vector(0, 0, 0), Vector(4, 1.5, 1), q3_mat)
        self.q3_cube_obsticle_2 = SimpleCube(shader, Point(-2.5, 0.2, 3),   Vector(0, 0, 0), Vector(3, 1.5, 2), q3_mat)
        self.q3_cube_obsticle_3 = SimpleCube(shader, Point(-0.5, 0.2, 4.5), Vector(0, 0, 0), Vector(1, 1.5, 5), q3_mat)

        # Quadrant 4
        self.q4_cube_obsticle_1 = SimpleCube(shader, Point(8.5, 0.2, 1.5), Vector(0, 0, 0), Vector(3, 1.5, 3), q4_mat)
        self.q4_cube_obsticle_2 = SimpleCube(shader, Point(6, 0.2, 2.5),   Vector(0, 0, 0), Vector(2, 1.5, 1), q4_mat)
        self.q4_cube_obsticle_3 = SimpleCube(shader, Point(0.5, 0.2, 4.5), Vector(0, 0, 0), Vector(1, 1.5, 5), q4_mat)
        self.q4_cube_obsticle_4 = SimpleCube(shader, Point(6.5, 0.2, 8.5), Vector(0, 0, 0), Vector(1, 1.5, 3), q4_mat)

        # Fill space up with crates for fun
        self.crate_1 = Crate(shader, Point(-9.75, -0.45, 3),    Vector(0, 0, 0),  Vector(0.15, 0.15, 0.15))
        self.crate_2 = Crate(shader, Point(-9.75, -0.45, 2.5),  Vector(0, 0, 0),  Vector(0.15, 0.15, 0.15))
        self.crate_3 = Crate(shader, Point(-9.43, -0.45, 2.75), Vector(0, 0, 0),  Vector(0.15, 0.15, 0.15))
        self.crate_4 = Crate(shader, Point(-9.75, -0.15, 2.75), Vector(0, 90, 0), Vector(0.15, 0.15, 0.15))

        # Fill the list with instances of Cube() that can then be drawn
        self.cubes = []

        self.cubes.append(self.wall1)
        self.cubes.append(self.wall2)
        self.cubes.append(self.wall3)
        self.cubes.append(self.wall4)

        self.cubes.append(self.q1_cube_obsticle_1)
        self.cubes.append(self.q1_cube_obsticle_2)
        self.cubes.append(self.q1_cube_obsticle_3)

        self.cubes.append(self.q2_cube_obsticle_1)
        self.cubes.append(self.q2_cube_obsticle_2)
        self.cubes.append(self.q2_cube_obsticle_3)
        self.cubes.append(self.q2_cube_obsticle_4)

        self.cubes.append(self.q3_cube_obsticle_1)
        self.cubes.append(self.q3_cube_obsticle_2)
        self.cubes.append(self.q3_cube_obsticle_3)

        self.cubes.append(self.q4_cube_obsticle_1)
        self.cubes.append(self.q4_cube_obsticle_2)
        self.cubes.append(self.q4_cube_obsticle_3)
        self.cubes.append(self.q4_cube_obsticle_4)

        self.cubes.append(self.crate_1)
        self.cubes.append(self.crate_2)
        self.cubes.append(self.crate_3)
        self.cubes.append(self.crate_4)

        self.destroy = False
        
    
    def collision(self, obj) -> GameObject:
        # Implement collision
        collision_walls = []
        for x in range(0, len(self.cubes)):
            c = self.cubes[x].collision(obj)
            if c is not None:
                collision_walls.append(c)
        if collision_walls == []:
            return None
        return collision_walls
    
    def draw(self, modelMatrix) -> None:
        # Implement the draw call
        for x in range(0, len(self.cubes)):
            c = self.cubes[x]
            c.draw(modelMatrix)

    def update(self, delta_time, game_objects):
        pass