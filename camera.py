import math
from ray import Ray
from vector3 import Vector3


class Camera:
    def __init__(self, position, fov):
        self.__position = position
        self.__fov = fov

    def calcRay(self, x, y, width, height):
        aspect_ratio = width / height
        angle = math.tan(math.pi * 0.5 * self.__fov / 180)
        x_norm = (2 * ((x + 0.5) / width) - 1) * angle * aspect_ratio
        y_norm = (1 - 2 * ((y + 0.5) / height)) * angle
        look_at = Vector3(x_norm, y_norm, 1).normalize()
        return Ray(self.__position, look_at)
