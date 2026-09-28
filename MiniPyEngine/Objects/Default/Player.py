import configparser
import math
import os
import pygame
from OpenGL.GL import *

try:
    from .Bullet.Bullet import Bullet
except ImportError:
    try:
        from Bullet.Bullet import Bullet
    except ImportError:
        Bullet = None

class Player:
    def __init__(self, position=None):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "../../config.cfg")

        def get_cfg(section, key, fallback, val_type=float):
            if self.config.has_option(section, key):
                try:
                    return val_type(self.config.get(section, key))
                except ValueError:
                    return fallback
            return fallback

        def get_str_cfg(section, key, fallback):
            if self.config.has_option(section, key):
                return self.config.get(section, key).strip().upper()
            return fallback

        spawn_x = get_cfg("PLAYER", "spawn_x", 0.0)
        spawn_y = get_cfg("PLAYER", "spawn_y", 1.0)
        spawn_z = get_cfg("PLAYER", "spawn_z", 5.0)

        if position is not None:
            if hasattr(position, 'x'):
                self.x, self.y, self.z = position.x, position.y, position.z
            else:
                self.x, self.y, self.z = position[0], position[1], position[2]
        else:
            self.x, self.y, self.z = (spawn_x, spawn_y, spawn_z)

        self.yaw = 0.0
        self.pitch = 0.0

        self.speed = get_cfg("PLAYER", "walk_speed", 5.0)
        self.run_speed = get_cfg("PLAYER", "run_speed", 9.0)
        self.crouch_speed = get_cfg("PLAYER", "crouch_speed", 2.5)
        self.sensitivity = get_cfg("ENGINE", "sensitivity", 40) / 300.0
        self.radius = get_cfg("PLAYER", "radius", 0.35)
        
        self.ammo = int(get_cfg("WEAPON", "ammo", 30))
        self.max_ammo = int(get_cfg("WEAPON", "max_ammo", 30))
        self.shoot_delay = get_cfg("WEAPON", "shot_delay", 0.12)
        self.damage = get_cfg("WEAPON", "damage", 25)
        self.range_val = get_cfg("WEAPON", "range", 500.0)

        self.hp = int(get_cfg("PLAYER", "max_health", 100))
        self.max_health = self.hp

        self.vel_y = 0.0
        self.gravity = get_cfg("PLAYER", "gravity", -18.0)
        self.jump_force = get_cfg("PLAYER", "jump_force", 6.5)
        self.is_grounded = True

        player_height = get_cfg("PLAYER", "height", 1.8)
        crouch_height = get_cfg("PLAYER", "crouch_height", 1.0)
        self.normal_y = self.y
        self.crouch_y = self.y - (player_height - crouch_height)
        self.is_crouching = False

        # Konsol Hile Bayrakları (Engine tarafından güncellenir)
        self.god = False
        self.noclip = False
        self.nojump = False
        self.nocrouch = False

        def get_key_constant(key_name, default_key):
            key_map = {
                "W": pygame.K_w, "S": pygame.K_s, "A": pygame.K_a, "D": pygame.K_d,
                "LSHIFT": pygame.K_LSHIFT, "RSHIFT": pygame.K_RSHIFT,
                "LCTRL": pygame.K_LCTRL, "RCTRL": pygame.K_RCTRL,
                "SPACE": pygame.K_SPACE, "F3": pygame.K_F3, "ESC": pygame.K_ESCAPE
            }
            return key_map.get(key_name, default_key)

        self.key_forward = get_key_constant(get_str_cfg("INPUT", "forward", "W"), pygame.K_w)
        self.key_backward = get_key_constant(get_str_cfg("INPUT", "backward", "S"), pygame.K_s)
        self.key_left = get_key_constant(get_str_cfg("INPUT", "left", "A"), pygame.K_a)
        self.key_right = get_key_constant(get_str_cfg("INPUT", "right", "D"), pygame.K_d)
        self.key_run = get_key_constant(get_str_cfg("INPUT", "run", "LSHIFT"), pygame.K_LSHIFT)
        self.key_jump = get_key_constant(get_str_cfg("INPUT", "jump", "SPACE"), pygame.K_SPACE)
        self.key_crouch = get_key_constant(get_str_cfg("INPUT", "crouch", "LCTRL"), pygame.K_LCTRL)

        self.shot_sound = None
        try:
            sound_path = os.path.join(os.path.dirname(__file__), "../../Sounds/Shot.mp3")
            if os.path.exists(sound_path):
                self.shot_sound = pygame.mixer.Sound(sound_path)
                self.shot_sound.set_volume(0.3)
        except Exception:
            pass

        self.shoot_cooldown = 0.0

    def handle_mouse_input(self):
        dx, dy = pygame.mouse.get_rel()
        self.yaw += dx * self.sensitivity
        self.pitch += dy * self.sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def take_damage(self, amount):
        if self.god:
            return
        self.hp = max(0, self.hp - amount)

    def check_collision(self, next_x, next_z, scene_objects):
        if self.noclip:
            return False

        for obj in scene_objects:
            pos = getattr(obj, 'position', (0, 0, 0))
            scale = getattr(obj, 'scale', (1, 1, 1))

            if hasattr(pos, 'x'): ox, oy, oz = pos.x, pos.y, pos.z
            else: ox, oy, oz = pos[0], pos[1], pos[2]

            if hasattr(scale, 'x'): sx, sy, sz = scale.x, scale.y, scale.z
            else: sx, sy, sz = scale[0], scale[1], scale[2]

            if "Floor" in type(obj).__name__:
                continue

            min_x = ox - (sx / 2.0) - self.radius
            max_x = ox + (sx / 2.0) + self.radius
            min_z = oz - (sz / 2.0) - self.radius
            max_z = oz + (sz / 2.0) + self.radius

            if min_x <= next_x <= max_x and min_z <= next_z <= max_z:
                return True  
        return False

    def update(self, dt, scene_objects, just_unpaused=False):
        # God Mode Aktifse Canı Daima Maksimumda Tut
        if self.god:
            self.hp = self.max_health

        self.handle_mouse_input()
        pygame.event.pump()

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        new_bullets = []

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        # Ateş etme mantığı (Unpause sonrası ilk tıklamayı engeller)
        if mouse_buttons[0] and self.shoot_cooldown <= 0 and not just_unpaused:
            if self.ammo > 0:
                self.ammo -= 1
                self.shoot_cooldown = self.shoot_delay
                if self.shot_sound:
                    self.shot_sound.play()
                
                pitch_rad = math.radians(self.pitch)
                yaw_rad = math.radians(self.yaw)
                f_x = math.sin(yaw_rad) * math.cos(pitch_rad)
                f_y = math.sin(pitch_rad)
                f_z = -math.cos(yaw_rad) * math.cos(pitch_rad)

                spawn_offset = 1.2
                bullet_pos = (
                    self.x + f_x * spawn_offset,
                    self.y + f_y * spawn_offset,
                    self.z + f_z * spawn_offset
                )
                bullet_rot = (self.pitch, self.yaw, 0.0)
                if Bullet:
                    bullet = Bullet(bullet_pos, bullet_rot, speed=150.0, damage=self.damage, range_val=self.range_val)
                    new_bullets.append(bullet)

        current_speed = self.speed
        if keys[self.key_run]:
            current_speed = self.run_speed
            self.is_crouching = False

        # NoCrouch kontrolü: Eğilme engellendiyse is_crouching True yapılmaz
        if keys[self.key_crouch] and not self.nocrouch:
            self.is_crouching = True
            current_speed = self.crouch_speed
        else:
            if not keys[self.key_run]:
                self.is_crouching = False

        target_y = self.crouch_y if self.is_crouching else self.normal_y
        move_speed = current_speed * dt

        rad_yaw = math.radians(self.yaw)
        forward_x = math.sin(rad_yaw)
        forward_z = -math.cos(rad_yaw)
        right_x = math.cos(rad_yaw)
        right_z = math.sin(rad_yaw)

        move_x = 0.0
        move_z = 0.0

        if keys[self.key_forward]:
            move_x += forward_x * move_speed
            move_z += forward_z * move_speed
        if keys[self.key_backward]:
            move_x -= forward_x * move_speed
            move_z -= forward_z * move_speed
        if keys[self.key_right]:
            move_x += right_x * move_speed
            move_z += right_z * move_speed
        if keys[self.key_left]:
            move_x -= right_x * move_speed
            move_z -= right_z * move_speed

        # NoClip Modu: Duvar Çarpışmaları ve Yerçekimi Devre Dışı (Serbest Uçuş)
        if self.noclip:
            self.vel_y = 0.0
            self.is_grounded = False

            # Dikey uçuş kontrolleri (Space yukarı, Ctrl aşağı)
            if keys[self.key_jump] and not self.nojump:
                self.y += move_speed
            if keys[self.key_crouch] and not self.nocrouch:
                self.y -= move_speed

            self.x += move_x
            self.z += move_z
        else:
            # Normal Fizik ve Çarpışma Modu (NoJump kontrolü eklendi)
            if keys[self.key_jump] and self.is_grounded and not self.nojump:
                self.vel_y = self.jump_force
                self.is_grounded = False

            if not self.is_grounded:
                self.vel_y += self.gravity * dt
                self.y += self.vel_y * dt

                if self.y <= target_y:
                    self.y = target_y
                    self.vel_y = 0.0
                    self.is_grounded = True
            else:
                crouch_smooth_speed = 12.0
                self.y += (target_y - self.y) * min(1.0, dt * crouch_smooth_speed)

            if move_x != 0:
                if not self.check_collision(self.x + move_x, self.z, scene_objects):
                    self.x += move_x

            if move_z != 0:
                if not self.check_collision(self.x, self.z + move_z, scene_objects):
                    self.z += move_z

        return new_bullets

    def apply_camera(self):
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glTranslatef(-self.x, -self.y, -self.z)

    @property
    def position(self):
        try:
            from Engine import Vector3
            return Vector3(self.x, self.y, self.z)
        except ImportError:
            return (self.x, self.y, self.z)

    @position.setter
    def position(self, value):
        if hasattr(value, 'x'):
            self.x, self.y, self.z = value.x, value.y, value.z
        elif isinstance(value, (tuple, list)) and len(value) >= 3:
            self.x, self.y, self.z = value[0], value[1], value[2]
