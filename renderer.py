import tracer


class Renderer:
    def __init__(self, threads):
        pass

    def render(self, scene, width, height, super_sampling=1):
        return tracer.render(scene, width, height)
