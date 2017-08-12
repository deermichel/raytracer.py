from vector3 import Vector3
from ray import Ray

MAX_RECURSION_DEPTH = 5


def trace(ray, scene, depth):
    # intersect
    hit_object = None
    hit_t, hit_point, hit_normal = float("inf"), None, None
    for object in scene:
        intersection = object.primitive.intersect(ray)
        if intersection and intersection[0] < hit_t:
            hit_object = object
            hit_t, hit_point, hit_normal = intersection

    if hit_object is None:
        return Vector3(2, 2, 2)  # bg color

    traced_color = Vector3()
    bias = 1e-4

    inside = False
    if ray.direction.dot(hit_normal) > 0.0:
        inside = True
        hit_normal = -1 * hit_normal

    if not hit_object.material.is_diffuse and depth < MAX_RECURSION_DEPTH:
        # reflective/refractive object
        facingRatio = -ray.direction.dot(hit_normal)
        fresnel = mix((1 - facingRatio) ** 3, 1, 0.1)
        reflection_ray = Ray(hit_point + hit_normal * bias, ray.direction.reflect(hit_normal).normalize())
        reflection = trace(reflection_ray, scene, depth + 1)
        refraction = Vector3()

        # transparent?
        if hit_object.material.transparency > 0:
            from_ior = 1.0 if inside else 1.1
            to_ior = 1.1 if inside else 1.0
            refraction_ray = Ray(hit_point - hit_normal * bias,
                                 ray.direction.refract(from_ior, to_ior, hit_normal).normalize())
            refraction = trace(refraction_ray, scene, depth + 1)

        traced_color = ((reflection * fresnel + refraction * (1 - fresnel) * hit_object.material.transparency)
                        .mul_comp(hit_object.material.surface_color))

    else:
        # diffuse object
        for light in filter(lambda obj: obj.is_light, scene):
            transmission = Vector3(1, 1, 1)
            light_direction = (light.primitive.position - hit_point).normalize()
            for other in filter(lambda obj: obj != light, scene):
                if other.primitive.intersect(Ray(hit_point + hit_normal * bias, light_direction)):
                    transmission = Vector3()
                    break
            traced_color = traced_color + (
                hit_object.material.surface_color
                .mul_comp(transmission)
                .mul_comp(light.material.emission_color) *
                max(0, hit_normal.dot(light_direction))
            )

    return traced_color + hit_object.material.emission_color


def render(scene, width, height):
    image = {}
    i = 0

    from camera import Camera
    camera = Camera(Vector3(z=0), 30)

    # trace
    for y in range(height):
        for x in range(width):
            ray = camera.calcRay(x, y, width, height)
            image[x, y] = trace(ray, scene, 0)
            i += 1
            if i % 10000 == 0:
                print("{0:.2f}%".format(i / float(width * height) * 100.0))

    return image


def mix(a, b, mix):
    return b * mix + a * (1 - mix)
