import sys
from maths.Material import Material
from .GameObjectBase import GameObject
from .meshes.ObjLoader import load_obj_file

class Crate(GameObject):
    def __init__(self, shader, position, rotation, scale, material=Material(), visible=True) -> None:
        super().__init__(shader, position, rotation, scale, material, visible)
        obj_file_path = sys.path[0] + "\\models"
        obj_file_name = "crate.obj"
        self.create_obj = load_obj_file(obj_file_path, obj_file_name)
    
    def draw(self, modelMatrix):
        self._draw(modelMatrix, self.create_obj)