import math
from material import Material
from vector3 import Vector3
from ray import Ray
from renderobject import RenderObject
from sphere import Sphere


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
        return Vector3()  # bg color

    traced_color = Vector3()
    bias = 0  # 1e-4

    inside = False
    if ray.direction.dot(hit_normal) > 0.0:
        inside = True
        hit_normal = -1 * hit_normal

    # diffuse object
    for light in filter(lambda object: object.is_light, scene):
        transmission = Vector3(1, 1, 1)
        light_direction = (light.primitive.position - hit_point).normalize()
        for object in filter(lambda object: object != light, scene):
            if object.primitive.intersect(Ray(hit_point + hit_normal * bias, light_direction)):
                transmission = Vector3()
                break
        traced_color = traced_color + hit_object.material.surface_color.mul_comp(transmission).mul_comp(light.material.emission_color) * max(0, hit_normal.dot(light_direction))

    return traced_color


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


light_mat = Material(emission_color=Vector3(3, 3, 3))
light_sphere = Sphere(Vector3(0, 20, 0), 3)
light_obj = RenderObject(light_sphere, light_mat)

ground_mat = Material(surface_color=Vector3(0.2, 0.2, 0.2))
ground_sphere = Sphere(Vector3(0, -10004, -20), 10000)
ground_obj = RenderObject(ground_sphere, ground_mat)

blue_mat = Material(surface_color=Vector3(0, 0, 0.6))
blue_sphere = Sphere(Vector3(0, 0, -20), 4)
blue_obj = RenderObject(blue_sphere, blue_mat)

scene = []
scene.append(light_obj)
scene.append(ground_obj)
scene.append(blue_obj)

width = 640
height = 480

image = render(scene, width, height)

# save ppm image
file = open("output.ppm", "w")
file.write("P3\n{0} {1}\n255\n".format(width, height))
for y in range(height):
    for x in range(width):
        file.write("{0} {1} {2} ".format(*image[x, y].to_rgb_color()))
file.close()
