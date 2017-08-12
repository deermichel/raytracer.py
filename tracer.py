from ray import Ray
from vector3 import Vector3


class Tracer:
    def __init__(self, max_recursion_depth=5, bias=1e-4):
        self.__max_recursion_depth = max_recursion_depth
        self.__bias = bias

    def trace(self, ray, scene):
        self.__scene = scene
        return self.__trace_recursively(ray, scene, 0)

    def __trace_recursively(self, ray, depth):
        hit_object, hit_point, hit_normal = self.__intersect(ray)
        if hit_object is None:
            return Vector3(2, 2, 2)  # horizon
        traced_color = Vector3()
        if not hit_object.material.is_diffuse and depth < self.__max_recursion_depth:
            traced_color = self.__trace_non_diffuse(ray, hit_object, hit_point, hit_normal, depth)
        else:
            traced_color = self.__trace_diffuse(hit_object, hit_point, hit_normal)
        return traced_color + hit_object.material.emission_color

    def __intersect(self, ray):
        hit_object = None
        hit_t, hit_point, hit_normal = float("inf"), None, None
        for obj in self.__scene:
            intersection = obj.primitive.intersect(ray)
            if intersection and intersection[0] < hit_t:
                hit_object = obj
                hit_t, hit_point, hit_normal = intersection
        return hit_object, hit_point, hit_normal

    def __trace_diffuse(self, hit_object, hit_point, hit_normal):
        summed_color = Vector3()
        for light in filter(lambda obj: obj.is_light, self.__scene):
            transmission = Vector3(1, 1, 1)
            light_direction = (light.primitive.position - hit_point).normalize()
            for other in filter(lambda obj: obj != light, self.__scene):
                if other.primitive.intersect(Ray(hit_point + self.__bias * hit_normal,
                                             light_direction)):
                    transmission = Vector3()
                    break
            summed_color = summed_color + (
                hit_object.material.surface_color
                .mul_comp(transmission)
                .mul_comp(light.material.emission_color) *
                max(0, hit_normal.dot(light_direction)))
        return summed_color

    def __trace_non_diffuse(self, ray, hit_object, hit_point, hit_normal, depth):
        inside = ray.direction.dot(hit_normal) > 0
        if inside:
            hit_normal = -hit_normal
        facing_ratio = -ray.direction.dot(hit_normal)
        fresnel = self.__mix((1 - facing_ratio) ** 3, 1, 0.1)
        reflection_ray = Ray(hit_point + self.__bias * hit_normal,
                             ray.direction.refract(hit_normal).normalize())
        reflection = self.__trace_recursively(reflection_ray, depth + 1)
        refraction = Vector3()

        # transparent?
        if hit_object.material.transparency > 0:
            from_ior = ray.current_ior if inside else hit_object.material.ior
            to_ior = hit_object.material.ior if inside else ray.current_ior
            refraction_ray = Ray(hit_point - self.__bias * hit_normal,
                                 ray.direction.refract(from_ior, to_ior, hit_normal)
                                 .normalize())
            refraction = self.__trace_recursively(refraction_ray, depth + 1)

        # mix according to fresnel
        return ((reflection * fresnel +
                refraction * (1 - fresnel) * hit_object.material.transparency)
                .mul_comp(hit_object.material.surface_color))

    def __mix(self, a, b, mix):
        return b * mix + a * (1 - mix)
