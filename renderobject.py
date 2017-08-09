class RenderObject:
    def __init__(self, primitive, material):
        self.__primitive = primitive
        self.__material = material

    @property
    def primitive(self):
        return self.__primitive

    @property
    def material(self):
        return self.__material

    @property
    def is_light(self):
        return self.__material.emission_color.length > 0.0
