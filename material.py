from vector3 import Vector3


class Material:
    def __init__(self, surface_color=Vector3(), emission_color=Vector3(),
                 reflectivity=0.0, transparency=0.0, ior=1.0):
        self.__surface_color = surface_color
        self.__emission_color = emission_color
        self.__reflectivity = reflectivity
        self.__transparency = transparency
        self.__ior = ior

    @property
    def surface_color(self):
        return self.__surface_color

    @property
    def emission_color(self):
        return self.__emission_color

    @property
    def transparency(self):
        return self.__transparency

    @property
    def is_diffuse(self):
        return self.__reflectivity == 0.0 and self.__transparency == 0.0

    @property
    def ior(self):
        return self.__ior
