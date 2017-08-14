class Ray:
    """Ray (/half-line) class"""

    def __init__(self, origin, direction):
        """Creates a new ray"""
        self.__origin = origin
        self.__direction = direction
        self.__current_ior = 1.0

    @property
    def origin(self):
        """Returns the origin of the ray"""
        return self.__origin

    @property
    def direction(self):
        """Returns the direction of the ray"""
        return self.__direction

    @property
    def current_ior(self):
        """Returns the current index of refraction of the ray"""
        return self.__current_ior
