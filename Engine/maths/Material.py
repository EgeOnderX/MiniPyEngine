from maths.Color import Color

class Material:
    def __init__(self, diffuse = None, specular = None, shininess = None, texture_id = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.shininess = 1 if shininess == None else shininess
        self.texture_id = -1 if texture_id == None else texture_id