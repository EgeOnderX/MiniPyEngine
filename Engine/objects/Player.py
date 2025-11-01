import json, pygame, os, subprocess, sys, threading, console
from typing import List
from pygame.locals import *
from random import randint
from maths.Material import Material
from maths.Point import Point
from maths.Vector import Vector
from .GameObjectBase import GameObject
from .GameObjects import GameObjects
from .Camera import Camera
from .Bullet import Bullet
from CONSTANTS import *
from console import ConsoleWindow
pygame.init()
pygame.mixer.init()
cwd = os.path.dirname(os.path.abspath(__file__))
sound_folder = os.path.join(cwd, "..", "sounds")
shot_sound = pygame.mixer.Sound(os.path.join(sound_folder, "shot.mp3"))
dead_sound = pygame.mixer.Sound(os.path.join(sound_folder, "dead.mp3"))
damage_sound = pygame.mixer.Sound(os.path.join(sound_folder, "damage.mp3"))
class Player(GameObject):
    """
    'Player' is a big class that handles all of the player interaction with the game,
    movement, shooting, looking around and collision logic
    """
    def __init__(self, shader, position=Point(0,0,0), sensitivity=20) -> None:
        super().__init__(shader, position, Vector(0,0,0), Vector(0,0,0), Material())
        # Camera object and vectors
        self.camera = Camera(shader, position)
        self.velocity = Vector(0, 0, 0)
        self.prev_position = position
        # Mouse position and variables
        self.change_vec = Vector(position.x, position.y, position.z)
        self.mouse_x = G_SCREEN_WIDTH / 2
        self.mouse_y = G_SCREEN_HEIGHT / 2
        self.first_mouse = True
        self.pitch = 0
        self.yaw = 0
        self.sensitivity = sensitivity
        # Keyboard variables
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.sprint_key_down = False
        # Console variables
        self.console_opened = False
        self.firing = False
        self.noclip=False
        self.nojump=False
        self.nocrouch=False
        # Bullets that the player shoots, so that he doesn't collide with his own bullets at the start
        self.owned_bullets = []
        weapons=[]
        # Respawn logic variables
        self.dead = False
        # Jumping, crouching, walking hp and gravity
        self.is_jumping = False
        self.speed = 3
        self.vertical_velocity = 0
        self.jump_strength = 5
        self.gravity = -15
        self.hp=100
        self.ground_y = position.y
        self.is_crouching = False
        self.crouch_height = -0.3
        self.standing_height = position.y
        # Config mumbo_jumbos
        self.load_config()
    def load_config(self):
        config_path = os.path.join(cwd, "..", "config")
        if not os.path.exists(config_path):
            print("[ERROR] No config file found.")
            return

        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("console(") and line.endswith(")"):
                    command = line[8:-1].strip('"').strip("'")
                    self.apply_command(command)

    def apply_command(self, command):
        if command == "god":
            self.hp = 9999
            print("[INFO] GOD MODE is on. HP:9999")
        elif command == "noclip":
            self.noclip = not self.noclip
            if self.noclip:
                print("[INFO] NOCLIP is on.")
            else :
                print("[INFO] NOCLIP is off.")
        elif command == "nojump":
            self.nojump = not self.nojump
            if self.nojump:
                print("[INFO] NOJUMP is on.")
            else :
                print("[INFO] NOJUMP is off.")
                
        elif command == "nocrouch":
            self.nocrouch = not self.nocrouch
            if self.nocrouch:
                print("[INFO] NOCROUCH is on.")
            else :
                print("[INFO] NOCROUCH is off.")
        else:
            print(f"[ERROR] Unkown command: {command}")
            
    def shoot(self, game_objects):
        self.firing = False
        direction_looking = self.camera.viewMatrix.get_matrix()
        direction_fire = Vector(direction_looking[2], -direction_looking[9], -direction_looking[0])
        bullet_pos = Point(self.position.x, self.camera.viewMatrix.eye.y, self.position.z)
        bullet_obj = Bullet(self.shader, bullet_pos, direction_fire)
        game_objects.add_object(bullet_obj)
        self.owned_bullets.append(bullet_obj)
        shot_sound.play()
    def update(self, delta_time, game_objects : GameObjects):
        """
        update() is, well... executed every update

        @param 'delta_time' - time difference between the previous and current frame
        @param 'game_objects' - the object that handles all of the game objects
        """
        # Crouch height logic
        if not self.is_jumping:
            if self.is_crouching:
                if self.nocrouch==True:
                    return
                self.speed=1.5
                self.camera.set_eye_position(Point(self.position.x, self.ground_y + self.crouch_height, self.position.z))
            else:
                self.camera.set_eye_position(Point(self.position.x, self.ground_y, self.position.z))

        if self.dead:
            self.crouch=False
            print("[INFO] Player is deadth")
            dead_sound.play()
            pygame.time.wait(5000)
            pygame.quit()

        else:
            # Player is alive, can move and play normally
            self.rotation.y = -self.yaw
            self.move(delta_time)
            self._handle_jump(delta_time)

            self.prev_position = self.position
            self.position = self.camera.viewMatrix.eye
            self.position = self.camera.viewMatrix.eye
            self.position.y = self.camera.viewMatrix.eye.y 
            self._mouse_controller(delta_time)
            self._keyboard_controller()

            # Check all game objects for collisions
            collision_objects = game_objects.check_collision(self)
            if collision_objects != []:
                self.collide(collision_objects)
            
            # Shooting logic
            if self.firing:
                self.shoot(game_objects)
            
            for bullet in self.owned_bullets:
                if bullet.destroy == True:
                    self.owned_bullets.remove(bullet)
            
            # Set shader variables for correct lighting
            self.shader.use()
            self.shader.set_view_matrix(self.camera.viewMatrix.get_matrix())
            self.shader.set_eye_position(self.camera.viewMatrix.eye)
    
    def open_console(self):
        self.console_opened = True
        def run_console():
            console = ConsoleWindow(self.apply_command)
            console.open()
        thread = threading.Thread(target=run_console)
        thread.daemon = True
        thread.start()

    def move(self, delta_time):
        """
        move() moves the player around, what more do you want?

        @param 'delta_time' - time difference between the previous and current frame
        """
        self.change_vec += self.velocity * delta_time * self.speed
        self.camera.move_position(self.change_vec)

    def collide(self, collision_objects : List[GameObject]):
        """
        collide() defines what should happen if the user is colliding with an object

        @param 'collision_objects' - List of objects that the user is currently colliding with
        """
        if self.noclip==True:
            return
        for collision_object in collision_objects:
            if type(collision_object) == Bullet:
                if collision_object not in self.owned_bullets:
                    if self.hp<10:
                        self.dead = True
                        self.hp=0
                        
                    else:
                        self.hp-=10
                        damage_sound.play()
                        print(self.hp)
            else:
                teleport_back = self.position
                if collision_object.collision_side[0] == 1 or collision_object.collision_side[1] == 1:
                    teleport_back.x = self.prev_position.x
                if collision_object.collision_side[2] == 1 or collision_object.collision_side[3] == 1:
                    teleport_back.z = self.prev_position.z
                self.camera.set_eye_position(teleport_back)

    def event_loop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                self.firing = True

        if event.type == pygame.KEYDOWN:
            if not self.console_opened:
                if event.key == K_F3:
                    print("[INFO] Console window is now active DO NOT CHEAT")
                    self.console_opened = True
                    self.open_console()
                if self.console_opened==True:
                    pass
            if event.key == K_w:
                self.W_key_down = True
            if event.key == K_s:
                self.S_key_down = True
            if event.key == K_d:
                self.D_key_down = True
            if event.key == K_a:
                self.A_key_down = True
            if event.key == K_LSHIFT:
                self.sprint_key_down = True
            if event.key == K_SPACE and not self.is_jumping:
                self.is_jumping = True
                self.vertical_velocity = self.jump_strength
            if event.key == K_LCTRL or event.key == K_RCTRL:
                self.is_crouching = True

        elif event.type == pygame.KEYUP:
            if event.key == K_w:
                self.W_key_down = False
            if event.key == K_s:
                self.S_key_down = False
            if event.key == K_d:
                self.D_key_down = False
            if event.key == K_a:
                self.A_key_down = False
            if event.key == K_LSHIFT:
                self.sprint_key_down = False
            if event.key == K_LCTRL or event.key == K_RCTRL:
                self.is_crouching = False
    def _keyboard_controller(self):
        """
        _keyboard_controller() handles what should happen if the user is pressing a key
        """

        if self.W_key_down:
            self.velocity.x = -1
        if self.S_key_down:
            self.velocity.x = 1
        if self.A_key_down:
            self.velocity.z = -1
        if self.D_key_down:
            self.velocity.z = 1
        if self.sprint_key_down:
            self.speed = 5
        else:
            self.speed = 3

        if (not self.W_key_down and not self.S_key_down):
            self.velocity.x = 0
        if (not self.D_key_down and not self.A_key_down):
            self.velocity.z = 0

    def _mouse_controller(self, delta_time):
        if pygame.mouse.get_focused():
            mouse_dx, mouse_dy = pygame.mouse.get_rel()

            x_diff = mouse_dx * self.sensitivity * delta_time
            y_diff = mouse_dy * self.sensitivity * delta_time

            last_pitch = self.pitch
            last_yaw = self.yaw

            self.yaw += x_diff
            self.pitch += y_diff

            # Limit the camera's vertical range
            self.pitch = max(-89, min(89, self.pitch))

            if self.yaw > 360:
                self.yaw -= 360
            if self.yaw < 0:
                self.yaw += 360

            self.camera.pitch(self.pitch - last_pitch)
            self.camera.turn(last_yaw - self.yaw)

            if self.first_mouse:
                pygame.mouse.get_rel()
                self.first_mouse = False

    def _handle_jump(self, delta_time):
        if self.nojump==True:
            return
        if self.is_jumping:
            self.vertical_velocity += self.gravity * delta_time
            new_y = self.camera.viewMatrix.eye.y + self.vertical_velocity * delta_time

            if new_y <= self.ground_y:
                new_y = self.ground_y
                self.is_jumping = False
                self.vertical_velocity = 0

            self.camera.set_eye_position(Point(self.position.x, new_y, self.position.z))
