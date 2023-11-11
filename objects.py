from imports import *
from vec import *

class Sphere:
    def __init__(self, position, radius, material):
        self.position = np.array(position)
        self.radius = radius
        self.material = material

    def get_norm(self, pos):
        return normalize(pos - self.position)

class Ground:
    def __init__(self, material):
        self.material = material

    def get_norm(self, pos):
        return np.array((0., 0., 1.))
