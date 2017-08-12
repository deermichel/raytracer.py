import math
from material import Material
from vector3 import Vector3
from ray import Ray
from renderobject import RenderObject
from sphere import Sphere

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
    inv_width = 1.0 / width
    inv_height = 1.0 / height
    fov = 30
    aspect_ratio = width / height
    angle = math.tan(math.pi * 0.5 * fov / 180.0)
    i = 0

    # trace
    for y in range(height):
        for x in range(width):
            x_norm = (2 * ((x + 0.5) * inv_width) - 1) * angle * aspect_ratio
            y_norm = (1 - 2 * ((y + 0.5) * inv_height)) * angle
            ray_origin = Vector3()
            ray_direction = Vector3(x_norm, y_norm, -1).normalize()
            ray = Ray(ray_origin, ray_direction)
            image[x, y] = trace(ray, scene, 0)
            i += 1
            if i % 10000 == 0:
                print("{0:.2f}%".format(i / float(width * height) * 100.0))

    return image


def mix(a, b, mix):
    return b * mix + a * (1 - mix)


light_mat = Material(emission_color=Vector3(3, 3, 3))
light_sphere = Sphere(Vector3(0, 20, -30), 3)
light_obj = RenderObject(light_sphere, light_mat)

ground_mat = Material(surface_color=Vector3(0.2, 0.2, 0.2))
ground_sphere = Sphere(Vector3(0, -10004, -20), 10000)
ground_obj = RenderObject(ground_sphere, ground_mat)

mat1 = Material(surface_color=Vector3(1, 0.32, 0.36), reflectivity=1, transparency=0.5)
sphere1 = Sphere(Vector3(z=-20), 4)
obj1 = RenderObject(sphere1, mat1)

mat2 = Material(surface_color=Vector3(0.9, 0.76, 0.46), reflectivity=1)
sphere2 = Sphere(Vector3(5, -1, -15), 2)
obj2 = RenderObject(sphere2, mat2)

mat3 = Material(surface_color=Vector3(0.65, 0.77, 0.97), reflectivity=1)
sphere3 = Sphere(Vector3(5, 0, -25), 3)
obj3 = RenderObject(sphere3, mat3)

mat4 = Material(surface_color=Vector3(0.9, 0.9, 0.9), reflectivity=1)
sphere4 = Sphere(Vector3(-5.5, 0, -15), 3)
obj4 = RenderObject(sphere4, mat4)

scene = []
scene.append(light_obj)
scene.append(ground_obj)
scene.extend([obj1, obj2, obj3, obj4])

width = 150
height = 100

image = render(scene, width, height)

# save ppm image
file = open("output.ppm", "w")
file.write("P3\n{0} {1}\n255\n".format(width, height))
for y in range(height):
    for x in range(width):
        file.write("{0} {1} {2} ".format(*image[x, y].to_rgb_color()))
file.close()
