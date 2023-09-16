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

renderer = Renderer(width, height)

red = Material([1, 0, 0.2])
green = Material([0, 1, 0.2])
sky_blue = [0, 0.5, 1]
renderer.add_object(Sphere([0, 3, 0], 1.0, red))
renderer.add_object(Sphere([1, 3, 1], 1.0, green))
renderer.add_object(Sphere([-1, 3, 1], 1.0, green))
renderer.set_sky_color(sky_blue)

pil_image = Image.fromarray(renderer.draw_image())

bitmap_image = pil_image.save('output.png')

