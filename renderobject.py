class RenderObject:
    """Renderable object"""

    def __init__(self, primitive, material):
        """Creates a new render object"""
        self.__primitive = primitive
        self.__material = material

    @property
    def primitive(self):
        """Returns the primitive of the object"""
        return self.__primitive

    @property
    def material(self):
        """Returns the material of the object"""
        return self.__material

    @property
    def is_light(self):
        """Returns whether the object is a light"""
        return self.__material.emission_color.length > 0.0
