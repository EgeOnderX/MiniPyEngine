import os
from Objects.TexturedCube.TexturedCube import TexturedCube

class Walls(TexturedCube):
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), texture_path=None):
        # Eğer harita dosyasından bir kaplama yolu (texture_path) gelmediyse,
        # kendi klasöründeki varsayılan 'longwall.png' dosyasını ayarla.
        if not texture_path:
            base_dir = os.path.dirname(__file__)
            texture_path = os.path.join(base_dir, "longwall.png")

        # Üst sınıf olan TexturedCube'un init metodunu çağırarak objeyi oluştur
        super().__init__(position, rotation, scale, texture_path)
