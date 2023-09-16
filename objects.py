from imports import *

class Sphere:
    def __init__(self, position, radius, material):
        self.position = np.array(position)
        self.radius = radius
        self.material = material
