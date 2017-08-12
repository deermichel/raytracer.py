from tracer import Tracer


class Renderer:
    def __init__(self, threads):
        pass

    def render(self, scene, camera, width, height, super_sampling=1):
        image = {}
        i = 0
        tracer = Tracer()
        for y in range(height):
            for x in range(width):
                ray = camera.calcRay(x, y, width, height)
                image[x, y] = tracer.trace(ray, scene)
                i += 1
                if i % 10000 == 0:
                    print("{0:.2f}%".format(i / float(width * height) * 100.0))
        return image
