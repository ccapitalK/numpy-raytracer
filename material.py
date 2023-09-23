from imports import *

class Material:
    def __init__(self, albedo, diffuse=0, ambient=1, specular=0, reflect=0, transparency=0, shiny=0.8):
        self.albedo = np.array(albedo)
        self.diffuse = diffuse
        self.specular = specular
        self.shiny = shiny
        self.ambient = ambient
        self.reflect = reflect
        self.transparency = transparency

    def get_color(self, diff, spec):
        light = diff * self.diffuse + (spec ** self.shiny) * self.specular + self.ambient
        return light * self.albedo
