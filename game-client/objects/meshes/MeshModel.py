from OpenGL.GL import *
import numpy

class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        # self.index_arrays = dict()
        self.mesh_materials = dict()
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()
        self.using_textures = False

    def add_vertex(self, mesh_id, position, normal, uv, use_uv=False):
        self.using_textures = use_uv
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        if use_uv:
            self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z, uv.x, uv.y]
        else:
            self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z]
        self.vertex_counts[mesh_id] += 1

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        self.materials[mat_id] = mat
    
    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
                self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
                glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id], dtype='float32'), GL_STATIC_DRAW)
                glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]
            shader.set_material_diffuse(material.diffuse)
            shader.set_material_specular(material.specular)
            shader.set_material_shininess(material.shininess)
            if self.using_textures:
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, material.texture_id)
                shader.set_material_shininess(25)
                shader.set_attrib_buffers_tex(self.vertex_buffer_ids[mesh_id])
            else:
                shader.set_attribute_buffers(self.vertex_buffer_ids[mesh_id])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)