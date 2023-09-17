#!/usr/bin/env python3

from PIL import Image
from imports import *
from renderer import *
from material import *
import sys

match len(sys.argv):
    case 2:
        width = height = int(sys.argv[1])
    case 3:
        width, height = (int(sys.argv[1]), int(sys.argv[2]))
    case _:
        width = height = 128

red = Material([1, 0, 0.2])
green = Material([0, 1, 0.2])
sky_blue = [0, 0.5, 1]

scene = Scene()
# scene.add_object(Sphere([0, 3, 0], 1.0, red))
# scene.add_object(Sphere([1, 3, 1], 1.0, green))
# scene.add_object(Sphere([-1, 3, 1], 1.0, green))
for x in range(-4, 5):
    for z in range(-4, 5):
        scene.add_object(Sphere([x, 5, z], 0.25, green))

renderer = Renderer(width, height, scene)

renderer.set_sky_color(sky_blue)

pil_image = Image.fromarray(renderer.draw_image())

bitmap_image = pil_image.save('output.png')
