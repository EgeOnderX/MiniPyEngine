import sys
import math
import os
import configparser
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from MapLoader import MapLoader
from Objects.Default.Player import Player

def get_xyz(obj_or_pos):
    if hasattr(obj_or_pos, 'x') and hasattr(obj_or_pos, 'y') and hasattr(obj_or_pos, 'z'):
        return float(obj_or_pos.x), float(obj_or_pos.y), float(obj_or_pos.z)
    if isinstance(obj_or_pos, (tuple, list)) and len(obj_or_pos) >= 3:
        return float(obj_or_pos[0]), float(obj_or_pos[1]), float(obj_or_pos[2])
    return 0.0, 0.0, 0.0


class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, (tuple, list, Vector3)):
            if isinstance(x, Vector3):
                self.x, self.y, self.z = x.x, x.y, x.z
            else:
                self.x = float(x[0]) if len(x) > 0 else 0.0
                self.y = float(x[1]) if len(x) > 1 else 0.0
                self.z = float(x[2]) if len(x) > 2 else 0.0
        else:
            self.x, self.y, self.z = float(x), float(y), float(z)

    def __getitem__(self, item): return (self.x, self.y, self.z)[item]
    def __iter__(self): return iter((self.x, self.y, self.z))
    def __len__(self): return 3

    def __add__(self, other):
        ox, oy, oz = get_xyz(other) if not isinstance(other, (int, float)) else (other, other, other)
        return Vector3(self.x + ox, self.y + oy, self.z + oz)

    def __sub__(self, other):
        ox, oy, oz = get_xyz(other) if not isinstance(other, (int, float)) else (other, other, other)
        return Vector3(self.x - ox, self.y - oy, self.z - oz)

    def __mul__(self, scalar): return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    def __truediv__(self, scalar): return Vector3(0, 0, 0) if scalar == 0 else Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def length(self): return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def normalize(self):
        l = self.length()
        return Vector3(0, 0, 0) if l == 0 else self / l

    def dot(self, other):
        ox, oy, oz = get_xyz(other)
        return self.x * ox + self.y * oy + self.z * oz

    def cross(self, other):
        ox, oy, oz = get_xyz(other)
        return Vector3(self.y * oz - self.z * oy, self.z * ox - self.x * oz, self.x * oy - self.y * ox)

    def to_tuple(self): return (self.x, self.y, self.z)
    def __repr__(self): return f"Vector3({self.x}, {self.y}, {self.z})"


class Transform:
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.position = Vector3(position)
        self.rotation = Vector3(rotation)
        self.scale = Vector3(scale)

    def apply_transformations(self):
        px, py, pz = get_xyz(self.position)
        rx, ry, rz = get_xyz(self.rotation)
        sx, sy, sz = get_xyz(self.scale)
        glTranslatef(px, py, pz)
        glRotatef(rx, 1, 0, 0)
        glRotatef(ry, 0, 1, 0)
        glRotatef(rz, 0, 0, 1)
        glScalef(sx, sy, sz)


class GameObject:
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.transform = Transform(position, rotation, scale)
        self.position = self.transform.position
        self.rotation = self.transform.rotation
        self.scale = self.transform.scale
        self.enabled = True

    def update(self, dt): pass
    def draw(self): pass


class MiniPyEngine:
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "config.cfg")
        if os.path.exists(config_path):
            self.config.read(config_path)
        else:
            alt_path = os.path.join(os.path.dirname(__file__), "settings.ini")
            if os.path.exists(alt_path):
                self.config.read(alt_path)

        def get_cfg(section, key, fallback, val_type=float):
            if self.config.has_option(section, key):
                try: return val_type(self.config.get(section, key))
                except ValueError: return fallback
            return fallback

        def get_bool_cfg(section, key, fallback):
            if self.config.has_option(section, key):
                return self.config.get(section, key).strip().lower() in ("true", "1", "yes", "on")
            return fallback

        def get_str_cfg(section, key, fallback):
            if self.config.has_option(section, key):
                return self.config.get(section, key).strip()
            return fallback

        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.width = int(get_cfg("ENGINE", "width", 1920, int))
        self.height = int(get_cfg("ENGINE", "height", 1080, int))
        self.display_size = (self.width, self.height)
        
        self.fullscreen = get_bool_cfg("ENGINE", "fullscreen", False)
        self.target_fps = int(get_cfg("ENGINE", "fps", 144, int))
        
        self.fov = get_cfg("ENGINE", "fov", 75.0)
        self.near_clip = get_cfg("ENGINE", "near_clip", 0.1)
        self.far_clip = get_cfg("ENGINE", "far_clip", 1000.0)

        self.ambient_strength = get_cfg("RENDER", "ambient_strength", 0.35)
        self.wireframe = get_bool_cfg("RENDER", "wireframe", False)
        self.show_fps = get_bool_cfg("RENDER", "show_fps", True)

        self.default_map = get_str_cfg("MAP", "default", "Maps/default.mpf")

        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.pause_title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 42, bold=True)

        self.weapons = ["Pistol", "Rifle", "Shotgun", "Sniper"]
        self.selected_weapon_index = 0
        self.just_unpaused = False

        self.menu_sound = None
        sound_dir = "Sounds"
        if os.path.exists(os.path.join(sound_dir, "Menu.mp3")):
            self.menu_sound = pygame.mixer.Sound(os.path.join(sound_dir, "Menu.mp3"))
            self.menu_sound.set_volume(0.2)

        self._text_cache = {}

        # ==========================================
        # CONSOLE VE HİLE SİSTEMİ BAŞLANGICI
        # ==========================================
        self.show_console = False           # Konsol açık mı?
        self.console_anim_progress = 0.0    # Yumuşak animasyon değeri (0.0 kapalı, 1.0 tam açık)
        self.console_input = ""             # Kullanıcının yazdığı metin
        self.console_history = []           # Komut geçmişi

        # Config'den Hile Durumlarını Okuma
        self.god = get_bool_cfg("CONSOLE", "god", False)
        self.noclip = get_bool_cfg("CONSOLE", "noclip", False)
        self.nojump = get_bool_cfg("CONSOLE", "nojump", False)
        self.nocrouch = get_bool_cfg("CONSOLE", "nocrouch", False)
        # ==========================================

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        light_position = [10.0, 30.0, 10.0, 1.0]  
        ambient = self.ambient_strength
        light_ambient = [ambient, ambient, ambient, 1.0]      
        light_diffuse = [0.9, 0.9, 0.9, 1.0]      

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

    def draw_crosshair(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        
        cx, cy = self.display_size[0] // 2, self.display_size[1] // 2
        size = 10
        glColor4f(1.0, 0.86, 0.0, 0.9)

        glLineWidth(2.5)
        glBegin(GL_LINES)
        glVertex2f(cx - size, cy)
        glVertex2f(cx + size, cy)
        glVertex2f(cx, cy - size)
        glVertex2f(cx, cy + size)
        glEnd()

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def render_hud_text(self, text, color, x, y, font_obj=None, align="left"):
        use_font = font_obj if font_obj else self.font
        cache_key = (text, color, id(use_font))

        if cache_key in self._text_cache:
            texture_id, width, height = self._text_cache[cache_key]
        else:
            text_surface = use_font.render(text, True, color)
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            width, height = text_surface.get_size()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

            if len(self._text_cache) > 200:
                for tid, _, _ in self._text_cache.values():
                    try: glDeleteTextures([tid])
                    except Exception: pass
                self._text_cache.clear()

            self._text_cache[cache_key] = (texture_id, width, height)

        render_x = x
        if align == "center":
            render_x = x - width // 2
        elif align == "right":
            render_x = x - width

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(render_x, y)
        glTexCoord2f(1, 0); glVertex2f(render_x + width, y)
        glTexCoord2f(1, 1); glVertex2f(render_x + width, y + height)
        glTexCoord2f(0, 1); glVertex2f(render_x, y + height)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        return width, height

    def draw_slot_box(self, x, y, size, is_selected=False):
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        bg_alpha = 0.45 if is_selected else 0.25
        glColor4f(1.0, 0.86, 0.0, bg_alpha)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + size, y)
        glVertex2f(x + size, y + size)
        glVertex2f(x, y + size)
        glEnd()

        if is_selected:
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glLineWidth(3.0)
        else:
            glColor4f(1.0, 0.86, 0.0, 0.85)
            glLineWidth(2.0)

        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + size, y)
        glVertex2f(x + size, y + size)
        glVertex2f(x, y + size)
        glEnd()

    def draw_armor_icon(self, slot_index, x, y, size):
        cx = x + size / 2.0
        cy = y + size / 2.0
        s = size

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 0.9, 0.2, 0.9)
        glLineWidth(2.2)

        if slot_index == 0:
            glBegin(GL_LINE_STRIP)
            for angle in range(0, 181, 15):
                rad = math.radians(angle)
                vx = cx + math.cos(rad) * (s * 0.3)
                vy = cy + math.sin(rad) * (s * 0.28)
                glVertex2f(vx, vy)
            glEnd()

            glBegin(GL_LINE_LOOP)
            glVertex2f(cx - s * 0.3, cy)
            glVertex2f(cx + s * 0.3, cy)
            glVertex2f(cx + s * 0.25, cy - s * 0.22)
            glVertex2f(cx - s * 0.25, cy - s * 0.22)
            glEnd()

            glBegin(GL_LINES)
            glVertex2f(cx - s * 0.2, cy - s * 0.08)
            glVertex2f(cx + s * 0.2, cy - s * 0.08)
            glEnd()

        elif slot_index == 1:
            glBegin(GL_LINE_LOOP)
            glVertex2f(cx - s * 0.12, cy + s * 0.3)
            glVertex2f(cx - s * 0.32, cy + s * 0.2)
            glVertex2f(cx - s * 0.25, cy - s * 0.05)
            glVertex2f(cx - s * 0.22, cy - s * 0.3)
            glVertex2f(cx + s * 0.22, cy - s * 0.3)
            glVertex2f(cx + s * 0.25, cy - s * 0.05)
            glVertex2f(cx + s * 0.32, cy + s * 0.2)
            glVertex2f(cx + s * 0.12, cy + s * 0.3)
            glVertex2f(cx, cy + s * 0.18)
            glEnd()

        elif slot_index == 2:
            glBegin(GL_LINE_LOOP)
            glVertex2f(cx - s * 0.22, cy + s * 0.3)
            glVertex2f(cx + s * 0.22, cy + s * 0.3)
            glVertex2f(cx + s * 0.20, cy - s * 0.3)
            glVertex2f(cx + s * 0.05, cy - s * 0.3)
            glVertex2f(cx, cy - s * 0.05)
            glVertex2f(cx - s * 0.05, cy - s * 0.3)
            glVertex2f(cx - s * 0.20, cy - s * 0.3)
            glEnd()

        elif slot_index == 3:
            lb_x = cx - s * 0.12
            glBegin(GL_LINE_LOOP)
            glVertex2f(lb_x - s * 0.08, cy + s * 0.25)
            glVertex2f(lb_x + s * 0.05, cy + s * 0.25)
            glVertex2f(lb_x + s * 0.05, cy - s * 0.25)
            glVertex2f(lb_x - s * 0.18, cy - s * 0.25)
            glVertex2f(lb_x - s * 0.18, cy - s * 0.12)
            glVertex2f(lb_x - s * 0.08, cy - s * 0.05)
            glEnd()

            rb_x = cx + s * 0.12
            glBegin(GL_LINE_LOOP)
            glVertex2f(rb_x - s * 0.05, cy + s * 0.25)
            glVertex2f(rb_x + s * 0.08, cy + s * 0.25)
            glVertex2f(rb_x + s * 0.08, cy - s * 0.05)
            glVertex2f(rb_x + s * 0.18, cy - s * 0.12)
            glVertex2f(rb_x + s * 0.18, cy - s * 0.25)
            glVertex2f(rb_x - s * 0.05, cy - s * 0.25)
            glEnd()

    def render_inventory_and_equipment(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)

        box_size = 64
        margin = 16
        start_y = self.display_size[1] // 2 + 80

        left_x = 40
        for i in range(4):
            y_pos = start_y - i * (box_size + margin)
            is_sel = (i == self.selected_weapon_index)
            self.draw_slot_box(left_x, y_pos, box_size, is_selected=is_sel)

        right_x = self.display_size[0] - 40 - box_size
        for i in range(4):
            y_pos = start_y - i * (box_size + margin)
            self.draw_slot_box(right_x, y_pos, box_size, is_selected=False)
            self.draw_armor_icon(i, right_x, y_pos, box_size)

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw_pause_menu(self, mouse_pos):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_TEXTURE_2D)

        glColor4f(0.0, 0.0, 0.0, 0.75)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.display_size[0], 0)
        glVertex2f(self.display_size[0], self.display_size[1])
        glVertex2f(0, self.display_size[1])
        glEnd()

        cx = self.display_size[0] // 2
        cy = self.display_size[1] // 2

        btn_w, btn_h = 260, 48
        res_x = cx - btn_w // 2
        res_y = cy + 10

        main_x = cx - btn_w // 2
        main_y = cy - 55

        gl_my = self.display_size[1] - mouse_pos[1]

        is_hover_res = (res_x <= mouse_pos[0] <= res_x + btn_w) and (res_y <= gl_my <= res_y + btn_h)
        is_hover_main = (main_x <= mouse_pos[0] <= main_x + btn_w) and (main_y <= gl_my <= main_y + btn_h)

        glColor4f(1.0, 0.86, 0.0, 0.4 if is_hover_res else 0.15)
        glBegin(GL_QUADS)
        glVertex2f(res_x, res_y)
        glVertex2f(res_x + btn_w, res_y)
        glVertex2f(res_x + btn_w, res_y + btn_h)
        glVertex2f(res_x, res_y + btn_h)
        glEnd()

        glColor4f(1.0, 0.86, 0.0, 1.0 if is_hover_res else 0.6)
        glLineWidth(2.5)
        glBegin(GL_LINE_LOOP)
        glVertex2f(res_x, res_y)
        glVertex2f(res_x + btn_w, res_y)
        glVertex2f(res_x + btn_w, res_y + btn_h)
        glVertex2f(res_x, res_y + btn_h)
        glEnd()

        glColor4f(1.0, 0.86, 0.0, 0.4 if is_hover_main else 0.15)
        glBegin(GL_QUADS)
        glVertex2f(main_x, main_y)
        glVertex2f(main_x + btn_w, main_y)
        glVertex2f(main_x + btn_w, main_y + btn_h)
        glVertex2f(main_x, main_y + btn_h)
        glEnd()

        glColor4f(1.0, 0.86, 0.0, 1.0 if is_hover_main else 0.6)
        glLineWidth(2.5)
        glBegin(GL_LINE_LOOP)
        glVertex2f(main_x, main_y)
        glVertex2f(main_x + btn_w, main_y)
        glVertex2f(main_x + btn_w, main_y + btn_h)
        glVertex2f(main_x, main_y + btn_h)
        glEnd()

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        self.render_hud_text("PAUSED", (255, 220, 0, 255), cx, cy + 85, self.pause_title_font, align="center")

        col_res = (255, 255, 255, 255) if is_hover_res else (220, 220, 220, 255)
        col_main = (255, 255, 255, 255) if is_hover_main else (220, 220, 220, 255)

        self.render_hud_text("Resume Game", col_res, cx, res_y + 12, self.font, align="center")
        self.render_hud_text("Exit to Menu", col_main, cx, main_y + 12, self.font, align="center")

        return (res_x, res_y, btn_w, btn_h), (main_x, main_y, btn_w, btn_h)

    # ==========================================
    # YENİ EKLENEN KONSOL KOMUT & ÇİZİM SİSTEMİ
    # ==========================================
    def execute_console_command(self, cmd_text):
        cmd = cmd_text.strip().lower()
        if not cmd:
            return

        self.console_history.append(f"> {cmd_text}")
        if len(self.console_history) > 15:
            self.console_history.pop(0)

        parts = cmd.split()
        base_cmd = parts[0]

        if base_cmd == "god":
            self.god = not self.god
            msg = f"God Mode: {'ON' if self.god else 'OFF'}"
            self.console_history.append(msg)
        elif base_cmd == "noclip":
            self.noclip = not self.noclip
            msg = f"NoClip: {'ON' if self.noclip else 'OFF'}"
            self.console_history.append(msg)
        elif base_cmd == "nojump":
            self.nojump = not self.nojump
            msg = f"NoJump: {'ON' if self.nojump else 'OFF'}"
            self.console_history.append(msg)
        elif base_cmd == "nocrouch":
            self.nocrouch = not self.nocrouch
            msg = f"NoCrouch: {'ON' if self.nocrouch else 'OFF'}"
            self.console_history.append(msg)
        elif base_cmd == "clear":
            self.console_history.clear()
        elif base_cmd == "help":
            self.console_history.append("Available: god, noclip, nojump, nocrouch, clear")
        else:
            self.console_history.append(f"Unknown command: '{base_cmd}'")

    def draw_console(self):
        # Eğer konsol tamamen kapalıysa çizme
        if self.console_anim_progress <= 0.0:
            return

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_TEXTURE_2D)

        # Animasyonlu Kaydırma Mesafesi:
        # 1.0 (tam açık) olunca yukarıdan c_height kadar iner
        c_height = self.display_size[1] // 2
        anim_y = self.display_size[1] + c_height - int(c_height * self.console_anim_progress * 2) 
        
        # Animasyon sınırını c_height kadar sınırlıyoruz (Taşmasını önlemek için)
        current_y_bottom = self.display_size[1] - int(c_height * self.console_anim_progress)

        # Konsol Arka Planı (Saydam Sarı Temalı)
        glColor4f(0.1, 0.09, 0.02, 0.85)  # Arka plan hafif sarımsı koyu gri
        glBegin(GL_QUADS)
        glVertex2f(0, current_y_bottom)
        glVertex2f(self.display_size[0], current_y_bottom)
        glVertex2f(self.display_size[0], self.display_size[1])
        glVertex2f(0, self.display_size[1])
        glEnd()

        # Alt Çizgi (Sarı Tema)
        glColor4f(1.0, 0.86, 0.0, 1.0)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        glVertex2f(0, current_y_bottom)
        glVertex2f(self.display_size[0], current_y_bottom)
        glEnd()

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        # Konsol geçmişini aşağıdan yukarıya doğru yazdır (Sadece animasyon oranına göre kayarak)
        start_y = current_y_bottom + 40
        for line in reversed(self.console_history):
            self.render_hud_text(line, (255, 235, 120, 255), 20, start_y, self.font)
            start_y += 26
            if start_y > self.display_size[1] - 30:
                break

        # Aktif Yazı Satırı (Giriş) - Sarı Renk
        prompt = f"> {self.console_input}_"
        self.render_hud_text(prompt, (255, 220, 0, 255), 20, current_y_bottom + 10, self.font)

    # ==========================================

    def run_game(self):
        flags = pygame.DOUBLEBUF | pygame.OPENGL
        if self.fullscreen:
            flags |= pygame.FULLSCREEN

        pygame.display.set_mode(self.display_size, flags)
        
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glShadeModel(GL_SMOOTH)

        if self.wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, (self.display_size[0] / self.display_size[1]), self.near_clip, self.far_clip)
        glMatrixMode(GL_MODELVIEW)

        self.setup_lighting()

        map_loader = MapLoader()
        scene_objects = map_loader.load_map(self.default_map) 

        player = Player()

        game_running = True
        paused = False

        while game_running:
            dt = self.clock.tick(self.target_fps) / 1000.0  
            if dt > 0.1: dt = 0.1

            # Konsol Animasyonu (Yumuşak Açılıp Kapanma)
            anim_speed = 5.0 * dt
            if self.show_console:
                self.console_anim_progress = min(1.0, self.console_anim_progress + anim_speed)
            else:
                self.console_anim_progress = max(0.0, self.console_anim_progress - anim_speed)

            mouse_pos = pygame.mouse.get_pos()
            gl_my = self.display_size[1] - mouse_pos[1]

            if not pygame.mouse.get_pressed()[0]:
                self.just_unpaused = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    # KONSOL AÇ/KAPAT (F3)
                    if event.key == pygame.K_F3:
                        self.show_console = not self.show_console
                        if self.show_console:
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                        elif not paused:
                            self.just_unpaused = True
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                        continue
                    
                    # Konsol Aktifken Yazı Yazma
                    if self.show_console:
                        if event.key == pygame.K_RETURN:
                            self.execute_console_command(self.console_input)
                            self.console_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.console_input = self.console_input[:-1]
                        elif event.unicode and event.key != pygame.K_ESCAPE and event.key != pygame.K_F3:
                            self.console_input += event.unicode
                        continue

                    # Pause (ESC) - Konsol açıkken çalışmasını engelliyoruz
                    if event.key == pygame.K_ESCAPE and not self.show_console:
                        paused = not paused
                        if paused:
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                        else:
                            self.just_unpaused = True
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                        if self.menu_sound: self.menu_sound.play()

                    if not paused and not self.show_console:
                        if event.key == pygame.K_1: self.selected_weapon_index = 0
                        elif event.key == pygame.K_2: self.selected_weapon_index = 1
                        elif event.key == pygame.K_3: self.selected_weapon_index = 2
                        elif event.key == pygame.K_4: self.selected_weapon_index = 3

                elif event.type == pygame.MOUSEWHEEL and not paused and not self.show_console:
                    if event.y > 0:
                        self.selected_weapon_index = (self.selected_weapon_index - 1) % len(self.weapons)
                    elif event.y < 0:
                        self.selected_weapon_index = (self.selected_weapon_index + 1) % len(self.weapons)

                elif event.type == pygame.MOUSEBUTTONDOWN and paused and not self.show_console:
                    if event.button == 1:
                        cx = self.display_size[0] // 2
                        cy = self.display_size[1] // 2
                        btn_w, btn_h = 260, 48
                        res_x, res_y = cx - btn_w // 2, cy + 10
                        main_x, main_y = cx - btn_w // 2, cy - 55

                        if res_x <= mouse_pos[0] <= res_x + btn_w and res_y <= gl_my <= res_y + btn_h:
                            paused = False
                            self.just_unpaused = True  
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                        elif main_x <= mouse_pos[0] <= main_x + btn_w and main_y <= gl_my <= main_y + btn_h:
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                            return

            # Pause ve Konsol (veya animasyonu) kapalıysa oyun çalışır
            if not paused and self.console_anim_progress == 0.0:
                
                # Konsol değişkenlerini oyuncuya paslama
                player.god = getattr(self, 'god', False)
                player.noclip = getattr(self, 'noclip', False)
                player.nojump = getattr(self, 'nojump', False)
                player.nocrouch = getattr(self, 'nocrouch', False)

                player.update(dt, scene_objects, just_unpaused=self.just_unpaused)

                px, py, pz = get_xyz(player.position)
                for obj in scene_objects[:]:
                    if obj.__class__.__name__ == "Ammo" and getattr(obj, 'enabled', True):
                        ox, oy, oz = get_xyz(getattr(obj, 'position', (0, 0, 0)))
                        dist = math.sqrt((px - ox)**2 + (py - oy)**2 + (pz - oz)**2)
                        if dist < 1.8:
                            player.ammo = min(player.max_ammo, player.ammo + 30)
                            scene_objects.remove(obj)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            player.apply_camera()

            glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 30.0, 10.0, 1.0])

            for obj in scene_objects:
                obj.draw()

            hp = getattr(player, 'hp', 100)
            max_health = getattr(player, 'max_health', 100)
            ammo = getattr(player, 'ammo', 30)

            if hp >= max_health * 0.8: hp_color = (0, 255, 0, 255)
            elif hp >= max_health * 0.4: hp_color = (255, 255, 0, 255)
            else: hp_color = (255, 0, 0, 255)

            self.render_hud_text(f"HP: {hp}", hp_color, 40, 40, self.large_font, align="left")
            self.render_hud_text(f"AMMO: {ammo}", (255, 220, 0, 255), self.display_size[0] - 40, 40, self.large_font, align="right")

            self.render_inventory_and_equipment()

            if not paused and self.console_anim_progress == 0.0:
                self.draw_crosshair()

            if self.show_fps:
                current_fps = int(self.clock.get_fps())
                self.render_hud_text(f"FPS: {current_fps}", (0, 255, 255, 255), 40, self.display_size[1] - 60)

            # Konsol Ekranının Çizimi (Yumuşak Saydamlık ve Kayma Animasyonlu)
            if self.console_anim_progress > 0.0:
                self.draw_console()
            elif paused:
                self.draw_pause_menu(mouse_pos)

            pygame.display.flip()
