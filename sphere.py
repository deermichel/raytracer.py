import math


class Sphere:
    def __init__(self, position, radius):
        self.__position = position
        self.__radius = radius

    @property
    def position(self):
        return self.__position

    def intersect(self, ray):
        # http://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection
        l = self.__position - ray.origin
        t_ca = l.dot(ray.direction)
        if t_ca < 0:
            return
        d_squared = l.dot(l) - t_ca ** 2
        radius_squared = self.__radius ** 2
        if d_squared > radius_squared:
            return
        t_hc = math.sqrt(radius_squared - d_squared)
        t = t_ca - t_hc
        if t < 0.0:
            t = t_ca + t_hc
        hit_point = ray.origin + t * ray.direction
        hit_normal = (hit_point - self.__position).normalize()
        return t, hit_point, hit_normal
