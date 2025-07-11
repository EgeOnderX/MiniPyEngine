from OpenGL.GL import *
from objects.meshes.MeshModel import MeshModel
from maths.Color import Color
from maths.Material import Material
from maths.Point import Point
from maths.Vector import Vector
import pygame
from maths.Point import Point2D

is_image_file = False

def load_mtl_file(file_location, file_name, mesh_model):
    # print("  Start loading MTL: " + file_name)
    mtl = None
    fin = open(file_location + "/" + file_name)
    global is_image_file
    is_image_file = False
    for line in fin.readlines():
        tokens = line.split()
        if len(tokens) == 0:
            continue
        if tokens[0] == "newmtl":
            # print("    Material: " + tokens[1])
            mtl = Material()
            mesh_model.add_material(tokens[1], mtl)
        elif tokens[0] == "Kd":
            mtl.diffuse = Color(float(tokens[1]), float(tokens[2]), float(tokens[3]))
        elif tokens[0] == "Ks":
            mtl.specular = Color(float(tokens[1]), float(tokens[2]), float(tokens[3]))
        elif tokens[0] == "Ns":
            mtl.shininess = float(tokens[1])
        elif tokens[0] == "map_Kd":
            image = pygame.image.load(tokens[1])
            tex_string = pygame.image.tostring(image, "RGBA", 1)
            img_width = image.get_width()
            img_height = image.get_height()
            tex_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
            # Generate a mipmap for the texture
            glGenerateMipmap(GL_TEXTURE_2D)
            mtl.texture_id = tex_id
            is_image_file = True

    # print("  Finished loading MTL: " + file_name)

def load_obj_file(file_location, file_name):
    # print("Start loading OBJ: " + file_name)
    mesh_model = MeshModel()
    current_object_id = None
    current_position_list = []
    current_normal_list = []
    current_uv_list = []
    fin = open(file_location + "/" + file_name)
    for line in fin.readlines():
        tokens = line.split()
        if len(tokens) == 0:
            continue
        if tokens[0] == "mtllib":
            load_mtl_file(file_location, tokens[1], mesh_model)
        elif tokens[0] == "o":
            # print("  Mesh: " + tokens[1])
            current_object_id = tokens[1]
            # current_position_list = []
            # current_normal_list = []
        elif tokens[0] == "v":
            current_position_list.append(Point(float(tokens[1]), float(tokens[2]), float(tokens[3])))
        elif tokens[0] == "vn":
            current_normal_list.append(Vector(float(tokens[1]), float(tokens[2]), float(tokens[3])))
        elif tokens[0] == "usemtl":
            mesh_model.set_mesh_material(current_object_id, tokens[1])
        elif tokens[0] == "vt":
            current_uv_list.append(Point2D(float(tokens[1]), float(tokens[2])))
        elif tokens[0] == "f":
            for i in range(1, len(tokens)):
                tokens[i] = tokens[i].split("/")
            vertex_count = len(tokens) - 1
            for i in range(vertex_count - 2):
                if current_position_list == None:
                    current_position_list = []
                if current_normal_list == None:
                    current_normal_list = []
                if is_image_file:
                    if current_uv_list == None:
                        current_uv_list = []
                # print(str(1) + " " + str(i+2) + " " + str(i+3))
                # print(int(tokens[i+3][0]))
                # print(int(tokens[i+3][2]))
                # print("size: " + str(len(current_position_list)))
                # print("size: " + str(len(current_normal_list)))
                # print(int(tokens[1][0])-1)
                # print(int(tokens[1][2])-1)
                mesh_model.add_vertex(current_object_id, current_position_list[int(tokens[1][0])-1], current_normal_list[int(tokens[1][2])-1], current_uv_list[int(tokens[1][1])-1], is_image_file)
                mesh_model.add_vertex(current_object_id, current_position_list[int(tokens[i+2][0])-1], current_normal_list[int(tokens[i+2][2])-1], current_uv_list[int(tokens[i+2][1])-1], is_image_file)
                mesh_model.add_vertex(current_object_id, current_position_list[int(tokens[i+3][0])-1], current_normal_list[int(tokens[i+3][2])-1], current_uv_list[int(tokens[i+3][1])-1], is_image_file)
    mesh_model.set_opengl_buffers()
    # print("Finished loading OBJ: " + file_name)
    return mesh_model