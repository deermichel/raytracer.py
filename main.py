# raytracer.py - basic Python raytracer
# Micha Hanselmann, 2017
# ---
# based on http://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-ray-tracing

from camera import Camera
from material import Material
from sphere import Sphere
from renderer import Renderer
from renderobject import RenderObject
from vector3 import Vector3

# render settings
width = 640
height = 480
super_sampling = 1

# create demo scene
light_mat = Material(emission_color=Vector3(4, 4, 4))
light_sphere = Sphere(Vector3(5, 50, 20), 5)
light_obj = RenderObject(light_sphere, light_mat)

light2_mat = Material(emission_color=Vector3(2, 2, 2))
light2_sphere = Sphere(Vector3(0, 10, -5), 5)
light2_obj = RenderObject(light2_sphere, light2_mat)

blue_light_mat = Material(emission_color=Vector3(0, 0, 1))
blue_light_sphere = Sphere(Vector3(-40, 5, 10), 3)
blue_light_obj = RenderObject(blue_light_sphere, blue_light_mat)

ground_mat = Material(surface_color=Vector3(0.2, 0.2, 0.2))
ground_sphere = Sphere(Vector3(0, -10010, 20), 10000)
ground_obj = RenderObject(ground_sphere, ground_mat)

mat1 = Material(surface_color=Vector3(0.8, 0.2, 0.2))
sph1 = Sphere(Vector3(10, 1, 50), 5)
obj1 = RenderObject(sph1, mat1)

mat2 = Material(surface_color=Vector3(1, 1, 1), transparency=1, ior=1.1)
sph2 = Sphere(Vector3(1, -1, 10), 1)
obj2 = RenderObject(sph2, mat2)

mat3 = Material(surface_color=Vector3(0.8, 0.8, 1), reflectivity=0.5, transparency=0.8)
sph3 = Sphere(Vector3(-4, -1, 20), 2)
obj3 = RenderObject(sph3, mat3)

mat4 = Material(surface_color=Vector3(1, 1, 1), reflectivity=1.0)
sph4 = Sphere(Vector3(0, 0, 60), 8)
obj4 = RenderObject(sph4, mat4)

scene = [ground_obj, light_obj, light2_obj, blue_light_obj, obj1, obj2, obj3, obj4]

# render
renderer = Renderer(tilesize=64)
camera = Camera(Vector3(), 30)
image = renderer.render(scene, camera, width, height, super_sampling)

# save ppm image
file = open("output.ppm", "w")
file.write("P3\n{0} {1}\n255\n".format(width, height))
for y in range(height):
    for x in range(width):
        file.write("{0} {1} {2} ".format(*image[x, y].to_rgb_color()))
file.close()
