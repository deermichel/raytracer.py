from tracer import Tracer
from vector3 import Vector3


class Renderer:
    """Renderer coordinating the tracing process"""

    def __init__(self, threads):
        """Creates a new renderer"""
        pass

    def render(self, scene, camera, width, height, super_sampling=1, logging=True):
        """Render a scene"""
        image = {}
        i = 0
        tracer = Tracer()
        for y in range(height):
            for x in range(width):
                sum_color = Vector3()
                sampled_rays = 0
                for ss_x in range(-super_sampling + 1, super_sampling):
                    for ss_y in range(-super_sampling + 1, super_sampling):
                        ray = camera.calcRay(x + ss_x, y + ss_y, width, height)
                        sum_color += tracer.trace(ray, scene)
                        sampled_rays += 1
                image[x, y] = sum_color * (1 / sampled_rays)
                if logging:
                    i += 1
                    if i % 1000 == 0:
                        print("{0:.2f}%".format(i / float(width * height) * 100.0))
        return image
