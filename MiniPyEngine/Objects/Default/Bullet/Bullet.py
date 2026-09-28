import math
import os
import pygame
from OpenGL.GL import *

class Bullet:
    def __init__(self, position, rotation, speed=150.0, damage=25, range_val=500.0):
        self.position = [float(position[0]), float(position[1]), float(position[2])]
        self.rotation = [float(rotation[0]), float(rotation[1]), float(rotation[2])]
        self.scale = (0.3, 0.3, 0.8)
        self.speed = speed
        self.damage = damage
        self.max_range = range_val
        self.distance_traveled = 0.0
        self.enabled = True

        pitch_rad = math.radians(self.rotation[0])
        yaw_rad = math.radians(self.rotation[1])

        self.dir_x = math.sin(yaw_rad) * math.cos(pitch_rad)
        self.dir_y = math.sin(pitch_rad)
        self.dir_z = -math.cos(yaw_rad) * math.cos(pitch_rad)

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.texture_id = None

        self.load_obj()
        self.load_texture()

    def load_obj(self):
        try:
            obj_path = os.path.join(os.path.dirname(__file__), "Bullet.obj")
            if os.path.exists(obj_path):
                with open(obj_path, "r") as f:
                    for line in f:
                        if line.startswith("#"):
                            continue
                        parts = line.split()
                        if not parts:
                            continue
                        if parts[0] == "v":
                            self.vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                        elif parts[0] == "vt":
                            self.texcoords.append([float(parts[1]), float(parts[2])])
                        elif parts[0] == "vn":
                            self.normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                        elif parts[0] == "f":
                            face = []
                            for p in parts[1:]:
                                vals = p.split("/")
                                vi = int(vals[0]) - 1
                                ti = int(vals[1]) - 1 if len(vals) > 1 and vals[1] != "" else -1
                                ni = int(vals[2]) - 1 if len(vals) > 2 and vals[2] != "" else -1
                                face.append((vi, ti, ni))
                            self.faces.append(face)
        except Exception as e:
            print(f"[WARNING] Failed to load Bullet.obj: {e}")

    def load_texture(self):
        try:
            tex_path = os.path.join(os.path.dirname(__file__), "Bullet.jpg")
            if os.path.exists(tex_path):
                surface = pygame.image.load(tex_path)
                surface = pygame.transform.flip(surface, False, True)
                img_data = pygame.image.tostring(surface, "RGB", True)
                width, height = surface.get_size()

                self.texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.texture_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        except Exception as e:
            print(f"[WARNING] Failed to load Bullet.jpg: {e}")

    def update(self, dt):
        if not self.enabled:
            return

        step = self.speed * dt
        self.position[0] += self.dir_x * step
        self.position[1] += self.dir_y * step
        self.position[2] += self.dir_z * step

        self.distance_traveled += step
        if self.distance_traveled >= self.max_range:
            self.enabled = False

    def draw(self):
        if not self.enabled:
            return

        glPushMatrix()
        glDisable(GL_LIGHTING) # Prevent lighting from making the bullet dark or invisible

        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[0], 1, 0, 0)
        glScalef(self.scale[0], self.scale[1], self.scale[2])

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(1.0, 0.8, 0.0) # Bright yellow fallback if texture missing

        if self.faces:
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for vi, ti, ni in face:
                    if ni >= 0 and ni < len(self.normals):
                        glNormal3fv(self.normals[ni])
                    if ti >= 0 and ti < len(self.texcoords):
                        glTexCoord2fv(self.texcoords[ti])
                    if vi >= 0 and vi < len(self.vertices):
                        glVertex3fv(self.vertices[vi])
            glEnd()
        else:
            s = 0.3
            glBegin(GL_QUADS)
            glVertex3f(-s, -s, s); glVertex3f(s, -s, s); glVertex3f(s, s, s); glVertex3f(-s, s, s)
            glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glEnable(GL_LIGHTING) # Re-enable lighting for the rest of the scene
        glPopMatrix()
