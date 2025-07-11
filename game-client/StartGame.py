import subprocess
import sys
import pygame
from typing import List
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from maths.Matricies import *
from maths.Lights import LightSource
from maths.Color import Color
from maths.Material import Material
from shaders.Shaders import Shader3D
from shaders.Crosshair import ShaderCrosshair
from objects.Floor import Floor
from objects.Enemy import Enemy
from objects.Bullet import Bullet
from objects.Level1 import Level1
from objects.Player import Player
from objects.GameObjects import GameObjects
from objects.meshes.ObjLoader import load_obj_file
from objects.primatives.Crosshair import Crosshair
from CONSTANTS import *
from networking.Networking import Networking
from misc.Config import Config

class StartGame:
    def __init__(self):
        self.is_networking = True

        self.config = Config()

        pygame.init()
        pygame.display.set_mode((self.config.screen_width, self.config.screen_height),pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)




        pygame.mouse.set_visible(False)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.get_rel()
        if self.is_networking:
            self.server = Networking(self.config.server_ip, self.config.server_port)
            if self.server.connect() == -1:
                self.is_networking = False

        
        self.shader = Shader3D()
        self.shader.use()

        crosshairshader = ShaderCrosshair()
        self.crosshair = Crosshair(crosshairshader)

        self.modelMatrix    = ModelMatrix()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.flat_shade = False

        self.angle = 0
        self.radius = 3
        self.light_x = self.radius
        self.light_z = self.radius

        self.fr_ticker = 0
        self.fr_sum = 0

        self.network_sum = 0
        self.network_cleanup_sum = 0
        self.enemy_list : List[Enemy] = []

    def initializeGameObjects(self):
        # Lights are not a part of game objects, but still need to be set in the shader
        g_ambient = Color(10/255, 10/255, 10/255, 1.0)

        self.light_yellow = LightSource(Point(9, 0, 9), Color(1.0, 193/255, 7/255, 1), Color(1.0, 193/255, 7/255, 1.0), g_ambient)
        self.light_yellow.set_light_in_shader(self.shader, 0)

        self.light_green = LightSource(Point(-9, 0, -9), Color(0.0, 250/255, 7/255, 1), Color(0.0, 250/255, 7/255, 1), g_ambient)
        self.light_green.set_light_in_shader(self.shader, 1)

        self.light_blue = LightSource(Point(-9, 0, 9), Color(5/255, 20/255, 250/255, 1), Color(5/255, 20/255, 250/255, 1), g_ambient)
        self.light_blue.set_light_in_shader(self.shader, 2)

        self.light_red = LightSource(Point(9, 0, -9), Color(240/255, 20/255, 7/255, 1), Color(240/255, 20/255, 7/255, 1), g_ambient)
        self.light_red.set_light_in_shader(self.shader, 3)

        # Setting rest of game objects
        self.level1 = Level1(self.shader, Point(-10, 0, -10))
        self.floor = Floor(self.shader, Point(0, -0.5, 0), Vector(0,0,0), Vector(20, 0.1, 20), Material())

        self.player = Player(self.shader, Point(9, 0, 9), sensitivity=self.config.sensitivity)
        if self.is_networking:
            init = self.server.do_initial_exchange()
            self.player.network_uid = init
        print("SENSITIVITY:", self.config.sensitivity)

        obj_file_path = sys.path[0] + "\\models"
        obj_file_name = "crate.obj"
        self.cube_obj = load_obj_file(obj_file_path, obj_file_name)
        
        # Game objects that should be in the scene
        # Note: The player is handled seperately from other objects
        self.game_objects = GameObjects()
        self.game_objects.add_object(self.level1)
        self.game_objects.add_object(self.floor)

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            # print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0

        if self.is_networking:
            self.network_sum += delta_time
            self.network_cleanup_sum += delta_time
            if self.network_sum > 1.0/120:
                # Networking code that handles spawning in new players when they connect
                # as well as updating their position etc.
                self.server.send(self.player.serialize())
                data : List[dict] = self.server.recv()
                if data != None:
                    for item in data:
                        if item["uid"] != self.player.network_uid:
                            item_in = False
                            for enemy in self.enemy_list:
                                if item["uid"] == enemy.network_uid:
                                    # Update the existing player info
                                    item_in = True
                                    obj_position = item["data"]["position"]
                                    obj_rotation = item["data"]["rotation"]
                                    enemy_pos = Point(obj_position["x"], obj_position["y"], obj_position["z"])
                                    enemy_rot = Vector(obj_rotation["x"], obj_rotation["y"], obj_rotation["z"])
                                    enemy.set_position(enemy_pos)
                                    enemy.rotation = enemy_rot
                                    enemy.visible = not item["data"]["dead"]
                                    enemy.disable_collision = item["data"]["dead"]
                                    bullet_l = item["data"]["bullets"]
                                    for b in bullet_l:
                                        bullet_pos = b["data"]["position"]
                                        bullet_dir = b["data"]["direction"]
                                        bp = Point(bullet_pos["x"], bullet_pos["y"], bullet_pos["z"])
                                        bd = Vector(bullet_dir["x"], bullet_dir["y"], bullet_dir["z"])
                                        new_b = Bullet(self.shader, bp, bd)
                                        new_b.network_uid = b["uid"]
                                        enemy.add_to_owned_bullets(new_b, self.game_objects)
                            if not item_in:
                                # Spawn a new player
                                obj_position = item["data"]["position"]
                                obj_rotation = item["data"]["rotation"]
                                enemy_pos = Point(obj_position["x"], obj_position["y"], obj_position["z"])
                                enemy_rot = Vector(obj_rotation["x"], obj_rotation["y"], obj_rotation["z"])
                                new_enemy = Enemy(self.shader, enemy_pos, enemy_rot, Vector(1, 1, 1), Material())
                                new_enemy.network_uid = item["uid"]
                                self.enemy_list.append(new_enemy)
                                self.game_objects.add_object(new_enemy)

                    if self.network_cleanup_sum > 2.0:
                        # Cleanup roughly every 2 seconds, mainly players that have disconnected
                        notfound = []
                        found = []
                        for enemy in self.enemy_list:
                            for item in data:
                                if item["uid"] == enemy.network_uid:
                                    found.append(enemy)
                                    if enemy in notfound:
                                        notfound.remove(enemy)
                                else:
                                    if enemy not in found:
                                        if enemy not in notfound:
                                            notfound.append(enemy)
                        if notfound != []:
                            self.game_objects.remove_object(notfound[0])
                            self.enemy_list.remove(notfound[0])
                        self.network_cleanup_sum = 0
                self.network_sum = 0

        # Update all objects in the scene, including the player
        self.game_objects.update_objects(delta_time)
        self.player.update(delta_time, self.game_objects)
    def display(self):
        # Make sure that the camera projection is in perspective
        self.player.camera.projection_matrix.set_perspective(3.14159/2, G_SCREEN_WIDTH/G_SCREEN_HEIGHT, 0.001, 100)
        
        if self.is_networking:
            glClearColor(66/255, 135/255, 245/255, 1.0)
        else:
            glClearColor(150/255, 25/255, 25/255, 1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_CLAMP)

        # Viewport'u orijinal sabit çözünürlükle ayarla
        glViewport(0, 0, G_SCREEN_WIDTH, G_SCREEN_HEIGHT)

        # Tüm oyun objelerini çiz
        self.game_objects.draw_objects(self.modelMatrix, self.shader, True)

        # Crosshair çizmek için ortografik moda geç
        self.player.camera.projection_matrix.set_orthographic(0, G_SCREEN_WIDTH, 0, G_SCREEN_HEIGHT, 0.01, 10)
        self.crosshair.draw()

        pygame.display.flip()

    def loop(self):
        exiting = False
        self.initializeGameObjects()
        
        while not exiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUITTING")
                    self.player.connected = False
                    subprocess.Popen(["py", "main.py"])  # ← Menüye geri dön
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("ESCAPING")
                        subprocess.Popen(["py", "main.py"])
                        self.player.connected = False
                        exiting = True
                    if event.key == K_x:
                        black = Color(0, 0, 0, 1)
                        self.shader.use()

                        self.flat_shade = not self.flat_shade
                        if self.flat_shade:
                            self.light_yellow.diffuse = Color(100/255, 100/255, 100/255, 1)
                            self.light_yellow.specular = Color(100/255, 100/255, 100/255, 1)
                            self.light_yellow.set_light_in_shader(self.shader, 0)

                            self.light_green.diffuse = Color(100/255, 100/255, 100/255, 1)
                            self.light_green.specular = Color(100/255, 100/255, 100/255, 1)
                            self.light_green.set_light_in_shader(self.shader, 1)

                            self.light_blue.diffuse = Color(100/255, 100/255, 100/255, 1)
                            self.light_blue.specular = Color(100/255, 100/255, 100/255, 1)
                            self.light_blue.set_light_in_shader(self.shader, 2)

                            self.light_red.diffuse = Color(100/255, 100/255, 100/255, 1)
                            self.light_red.specular = Color(100/255, 100/255, 100/255, 1)
                            self.light_red.set_light_in_shader(self.shader, 3)
                        else:
                            g_ambient = Color(10/255, 10/255, 10/255, 1.0)

                            self.light_yellow = LightSource(Point(9, 0, 9), Color(1.0, 193/255, 7/255, 1), Color(1.0, 193/255, 7/255, 1.0), g_ambient)
                            self.light_yellow.set_light_in_shader(self.shader, 0)

                            self.light_green = LightSource(Point(-9, 0, -9), Color(0.0, 250/255, 7/255, 1), Color(0.0, 250/255, 7/255, 1), g_ambient)
                            self.light_green.set_light_in_shader(self.shader, 1)

                            self.light_blue = LightSource(Point(-9, 0, 9), Color(5/255, 20/255, 250/255, 1), Color(5/255, 20/255, 250/255, 1), g_ambient)
                            self.light_blue.set_light_in_shader(self.shader, 2)

                            self.light_red = LightSource(Point(9, 0, -9), Color(240/255, 20/255, 7/255, 1), Color(240/255, 20/255, 7/255, 1), g_ambient)
                            self.light_red.set_light_in_shader(self.shader, 3)

                self.player.event_loop(event)

            self.update()
            self.display()
        
        # End of game loop
        pygame.quit()
    
    def start(self):
        if self.is_networking:
            if self.server.connected:
                self.loop()
        else:
            self.loop()

if __name__ == "__main__":
    s = StartGame()
    s.start()
