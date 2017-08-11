class Ray:
    def __init__(self, origin, direction):
        self.__origin = origin
        self.__direction = direction
        self.__current_ior = 1.1  # 1.0

    @property
    def origin(self):
        return self.__origin

    @property
    def direction(self):
        return self.__direction

    @property
    def current_ior(self):
        return self.__current_ior
