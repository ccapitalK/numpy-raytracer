#!/usr/bin/env python3

from PIL import Image
from imports import *
from renderer import *
import material
from scene import *

import random
import sys

match len(sys.argv):
    case 2:
        width = height = int(sys.argv[1])
    case 3:
        width, height = (int(sys.argv[1]), int(sys.argv[2]))
    case _:
        width = height = 128

red = material.Material([1, 0, 0.2])
green = material.Material([0, 1, 0.2])
ground = material.Material([0.5, 0.5, 0.7])
sky_blue_gradient = np.array([[0, 0.1, 0.8], [0, 0.5, 1]])

random.seed(1337)

def rand_sphere():
    # TODO: Better choice here, maybe using hsv instead?
    r = random.uniform(0.3, 0.7)
    g = random.uniform(0.3, 0.7)
    b = random.uniform(0.3, 0.7)
    x = random.gauss(0, 50)
    y = random.gauss(0, 50)
    reflect = max(0, random.uniform(-0.2, 0.8))
    size = random.uniform(0.5, 2)
    z = GROUND_Z + size
    pos = np.array([x, y, z])
    mat = material.Material([r, g, b], reflect=reflect, diffuse=0.3)
    return Sphere(pos, size, mat)

scene = Scene(ground)
scene.set_light([0, 0, 1000])
for i in range(500):
    scene.add_object(rand_sphere())

renderer = Renderer(width, height, scene)

renderer.set_sky_colors(sky_blue_gradient)

pil_image = Image.fromarray(renderer.draw_image())

bitmap_image = pil_image.save('output.png')
