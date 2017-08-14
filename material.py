from vector3 import Vector3


class Material:
    """Material class"""

    def __init__(self, surface_color=Vector3(), emission_color=Vector3(),
                 reflectivity=0.0, transparency=0.0, ior=1.0):
        """Creates a new material"""
        self.__surface_color = surface_color
        self.__emission_color = emission_color
        self.__reflectivity = reflectivity
        self.__transparency = transparency
        self.__ior = ior

    @property
    def surface_color(self):
        """Returns the surface color of the material"""
        return self.__surface_color

    @property
    def emission_color(self):
        """Returns the emission color of the material"""
        return self.__emission_color

    @property
    def transparency(self):
        """Returns the transparency of the material"""
        return self.__transparency

    @property
    def is_diffuse(self):
        """Returns whether the material is diffuse"""
        return self.__reflectivity == 0.0 and self.__transparency == 0.0

    @property
    def ior(self):
        """Returns the index of refraction of the material"""
        return self.__ior
