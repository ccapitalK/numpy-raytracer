#!/usr/bin/env python3

from PIL import Image
from imports import *
from renderer import *
import sys

match len(sys.argv):
    case 2:
        width = height = int(sys.argv[1])
    case 3:
        width, height = (int(sys.argv[1]), int(sys.argv[2]))
    case _:
        width = height = 128

renderer = Renderer(width, height)
pil_image = Image.fromarray(renderer.draw_image())

bitmap_image = pil_image.save('output.png')

