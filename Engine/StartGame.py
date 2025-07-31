import subprocess, sys, pygame, console, time
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
from objects.Bullet import Bullet
from objects.Level1 import Level1
from objects.Player import Player
from objects.GameObjects import GameObjects
from objects.meshes.ObjLoader import load_obj_file
from objects.primatives.Crosshair import Crosshair
from CONSTANTS import *
from misc.Config import Config
from console import ConsoleWindow
class StartGame:
    def __init__(self):
        self.config = Config()
        pygame.init()
        pygame.display.set_mode((self.config.screen_width, self.config.screen_height),pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        print("[INFO] pygame.mouse.set_visible(False)")
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.game_objects = GameObjects()
        print("[INFO] pygame.event.set_grab(True)")
        pygame.mouse.get_rel()
        self.shader = Shader3D()
        self.shader.use()
        crosshairshader = ShaderCrosshair()
        self.crosshair = Crosshair(crosshairshader)
        self.modelMatrix    = ModelMatrix()
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.flat_shade = False
        print("[INFO] self.flat_shade = False")
        self.angle = 0
        self.radius = 3
        self.light_x = self.radius
        self.light_z = self.radius
        self.fr_ticker = 0
        self.fr_sum = 0
        self.network_sum = 0
        self.network_cleanup_sum = 0
    def open_console_window(self):
        subprocess.Popen([sys.executable, "console.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

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

        self.level1 = Level1(self.shader, Point(-10, 0, -10))
        self.floor = Floor(self.shader, Point(0, -0.5, 0), Vector(0,0,0), Vector(20, 0.1, 20), Material())

        self.player = Player(self.shader, Point(9, 0, 9), sensitivity=self.config.sensitivity)
        print("[INFO] SENSITIVITY:", self.config.sensitivity)

        obj_file_path = sys.path[0] + "\\models"
        obj_file_name = "crate.obj"
        self.cube_obj = load_obj_file(obj_file_path, obj_file_name)
        self.game_objects = GameObjects()
        self.game_objects.add_object(self.level1)
        self.game_objects.add_object(self.floor)
        print("initializeGameObjects [OK]")
    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        self.game_objects.update_objects(delta_time)
        self.player.update(delta_time, self.game_objects)
    def display(self):
        self.player.camera.projection_matrix.set_perspective(3.14159/2, G_SCREEN_WIDTH/G_SCREEN_HEIGHT, 0.001, 100)
        glClearColor(66/255, 135/255, 245/255, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_CLAMP)
        glViewport(0, 0, G_SCREEN_WIDTH, G_SCREEN_HEIGHT)
        self.game_objects.draw_objects(self.modelMatrix, self.shader, True)
        self.player.camera.projection_matrix.set_orthographic(0, G_SCREEN_WIDTH, 0, G_SCREEN_HEIGHT, 0.01, 10)
        self.crosshair.draw()
        pygame.display.flip()
    def loop(self):
        exiting = False
        self.initializeGameObjects()    
        
        while not exiting:
            for event in pygame.event.get():
                self.player.event_loop(event,)
                if event.type == pygame.QUIT:
                    pygame.time.wait(50)
                    print("[INFO] QUITTING")
                    self.player.connected = False
                    subprocess.Popen(["py", "main.py"])
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.time.wait(50)
                        print("[INFO] ESCAPING")
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
        pygame.quit()
    
    def start(self):
        self.loop()

if __name__ == "__main__":
    s = StartGame()
    s.start()
