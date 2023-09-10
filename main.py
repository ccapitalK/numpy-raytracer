#!/usr/bin/env python3

try:
    import cupy as np
except:
    print("Cupy not found/installed, falling back to numpy")
    import numpy as np

from PIL import Image

WIDTH = 256
HEIGHT = 256

class Renderer:
    def __init__(self):
        self.colour = np.zeros(3)
        self.bitmap_data = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)

    def calc_pixel(self, x, y):
        self.colour[1] = y / WIDTH
        return 255 * self.colour

    def scene_dist(self, pos):
        "Min dist from position to a surface in the scene"
        pass

    def draw_image(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.bitmap_data[y][x][:] = self.calc_pixel(x, y)
        return self.bitmap_data

renderer = Renderer()
pil_image = Image.fromarray(renderer.draw_image())

bitmap_image = pil_image.save('output.png')

