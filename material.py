from imports import *

class Material:
    def __init__(self, albedo, diffuse=0, ambient=0.5, specular=0, reflect=0, transparency=0):
        self.albedo = np.array(albedo)
        self.diffuse = diffuse
        self.specular = specular
        self.ambient = specular
        self.reflect = reflect
        self.transparency = transparency

    def get_color(self, diff, spec):
        light = diff * self.diffuse + spec * self.specular + self.ambient
        return light * self.albedo
