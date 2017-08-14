# raytracer.py - basic Python raytracer
# Micha Hanselmann, 2017
# ---
# based on http://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-ray-tracing

import os
from camera import Camera
from material import Material
from sphere import Sphere
from renderer import Renderer
from renderobject import RenderObject
from vector3 import Vector3

# render settings
width = 300
height = 200
super_sampling = 2

# create demo scene
light_mat = Material(emission_color=Vector3(3, 3, 3))
light_sphere = Sphere(Vector3(0, 20, 30), 3)
light_obj = RenderObject(light_sphere, light_mat)

ground_mat = Material(surface_color=Vector3(0.2, 0.2, 0.2))
ground_sphere = Sphere(Vector3(0, -10004, 20), 10000)
ground_obj = RenderObject(ground_sphere, ground_mat)

mat1 = Material(surface_color=Vector3(1, 0.32, 0.36), reflectivity=1, transparency=0.5, ior=1.1)
sphere1 = Sphere(Vector3(z=20), 4)
obj1 = RenderObject(sphere1, mat1)

mat2 = Material(surface_color=Vector3(0.9, 0.76, 0.46), reflectivity=1)
sphere2 = Sphere(Vector3(5, -1, 15), 2)
obj2 = RenderObject(sphere2, mat2)

mat3 = Material(surface_color=Vector3(0.65, 0.77, 0.97), reflectivity=1)
sphere3 = Sphere(Vector3(5, 0, 25), 3)
obj3 = RenderObject(sphere3, mat3)

mat4 = Material(surface_color=Vector3(0.9, 0.9, 0.9), reflectivity=1)
sphere4 = Sphere(Vector3(-5.5, 0, 15), 3)
obj4 = RenderObject(sphere4, mat4)

scene = [ground_obj, obj1, obj2, obj3, obj4, light_obj]

# render
renderer = Renderer(os.cpu_count())
camera = Camera(Vector3(), 30)
image = renderer.render(scene, camera, width, height, super_sampling)

# save ppm image
file = open("output.ppm", "w")
file.write("P3\n{0} {1}\n255\n".format(width, height))
for y in range(height):
    for x in range(width):
        file.write("{0} {1} {2} ".format(*image[x, y].to_rgb_color()))
file.close()
