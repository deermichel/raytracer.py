import math


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.__x = x
        self.__y = y
        self.__z = z

    def __str__(self):
        return "Vector3({0}, {1}, {2})".format(self.__x, self.__y, self.__z)

    __repr__ = __str__

    def __add__(self, other):
        return Vector3(self.__x + other.__x,
                       self.__y + other.__y,
                       self.__z + other.__z)

    def __sub__(self, other):
        return self + other * -1

    def __mul__(self, factor):
        return Vector3(self.__x * factor,
                       self.__y * factor,
                       self.__z * factor)

    __rmul__ = __mul__

    @property
    def length(self):
        return math.sqrt(self.__x ** 2 + self.__y ** 2 + self.__z ** 2)

    def normalize(self):
        length = self.length
        if length == 0.0:
            return self
        return (1.0 / length) * self

    def dot(self, other):
        return (self.__x * other.__x +
                self.__y * other.__y +
                self.__z * other.__z)

    def to_rgb_color(self):
        r = max(0, min(1, self.__x)) * 255
        g = max(0, min(1, self.__y)) * 255
        b = max(0, min(1, self.__z)) * 255
        return int(r), int(g), int(b)

    def mul_comp(self, other):
        return Vector3(self.__x * other.__x,
                       self.__y * other.__y,
                       self.__z * other.__z)
