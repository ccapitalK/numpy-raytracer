from imports import *

class Material:
    def __init__(self, albedo, diffuse=0, specular=0, reflect=0, transparency=0):
        self.albedo = np.array(albedo)
        self.diffuse = diffuse
        self.specular = specular
        self.reflect = reflect
        self.transparency = transparency
