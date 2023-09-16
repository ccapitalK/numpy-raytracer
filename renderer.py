#!/usr/bin/env python3

from imports import *
from vec import *

HFOV_DEGREES = 90
HFOV = (HFOV_DEGREES / 180) * m.pi

_clip01_min = np.array([0])
_clip01_max = np.array([1])
def clip01(v):
    return np.clip(v, _clip01_min, _clip01_max)

def calc_edge_rays(vfov_ratio):
    assert(30 <= HFOV_DEGREES <= 150)
    x_extent = m.tan(HFOV / 2)
    z_extent = vfov_ratio * x_extent
    return [np.array([
        xm * x_extent,
        1,
        zm * z_extent,
        ]) for xm in [-1, 1] for zm in [-1, 1]]

class Sphere:
    def __init__(self):
        self.position = np.array([0, 3, 0])
        self.radius = 1.0

_zero3 = np.array([0, 0, 0])

class Renderer:
    def __init__(self, width, height):
        width = int(width)
        height = int(height)
        self.colour = np.zeros(3)
        self.bitmap_data = np.zeros((width, height, 3), dtype=np.uint8)
        self.width = width
        self.height = height
        self.scene = [Sphere()]
        self.camera_edge_rays = calc_edge_rays(height / width)

    def calc_pixel(self, x, y):
        # self.colour[1] = y / self.width
        ray = self.cast_ray_from_camera(x/self.width, y/self.height)
        return 255 * clip01(self.cast_ray(_zero3, ray))

    def cast_ray(self, pos, dir):
        "Cast ray from pos in dir (dir should be normalized)"
        while True:
            min_dist = self.scene_dist(pos)
            if min_dist > 1e3:
                # Assume way past edge of scene
                return _zero3
            if min_dist < 1e-3:
                return [1, 1, 1]
            pos = pos + dir * min_dist

    def scene_dist(self, pos):
        "Min signed dist from position to a surface in the scene"
        min_dist = m.inf
        for sphere in self.scene:
            min_dist = min(min_dist, dist(pos, sphere.position) - sphere.radius)
        return min_dist

    def cast_ray_from_camera(self, xfrac, yfrac):
        # TODO optimize
        r = self.camera_edge_rays
        h0 = lerp(r[0], r[1], xfrac)
        h1 = lerp(r[2], r[3], xfrac)
        return normalize(lerp(h0, h1, yfrac))

    def draw_image(self):
        for x in range(self.width):
            for y in range(self.height):
                self.bitmap_data[y][x][:] = self.calc_pixel(x, y)
        return self.bitmap_data

if __name__ == '__main__':
    print("Running tests")
    assert(FEQ(dist(calc_edge_rays(1)[0], (-1, 1, -1)), 0))
    assert(FEQ(dist(calc_edge_rays(2)[0], (-1, 1, -2)), 0))
    renderer = Renderer(16, 16)
    assert(FEQ(dist(renderer.cast_ray_from_camera(0.5, 0.5), (0, 1, 0)), 0))
    print("All tests passed")
