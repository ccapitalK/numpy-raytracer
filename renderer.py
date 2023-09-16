#!/usr/bin/env python3

from imports import *
from vec import *
from objects import *
from scene import *

HFOV_DEGREES = 90
HFOV = (HFOV_DEGREES / 180) * m.pi

def calc_edge_rays(vfov_ratio):
    assert(30 <= HFOV_DEGREES <= 150)
    x_extent = m.tan(HFOV / 2)
    z_extent = vfov_ratio * x_extent
    return [np.array([
        xm * x_extent,
        1,
        zm * z_extent,
        ]) for xm in [-1, 1] for zm in [-1, 1]]

def make_edgeray_matrix(edgerays):
    return np.concatenate(edgerays).reshape((4,3))

class Renderer:
    def __init__(self, width, height):
        width = int(width)
        height = int(height)
        self.colour = np.zeros(3)
        self.bitmap_data = np.zeros((height, width, 3), dtype=np.uint8)
        self.width = width
        self.height = height
        self.scene = Scene()
        self.camera_edge_rays = calc_edge_rays(width / height)
        self.camera_edgeray_matrix = make_edgeray_matrix(self.camera_edge_rays)
        self.sky = c_zero3

    def set_sky_color(self, color):
        self.sky = np.array(color)

    def add_object(self, o):
        self.scene.add_object(o)

    def calc_pixel(self, x, y):
        self.colour[1] = y / self.width
        ray = self.cast_ray_from_camera(x/self.width, y/self.height)
        return 255 * clip01(self.cast_ray(c_zero3, ray))

    def cast_ray(self, pos, dir):
        "Cast ray from pos in dir (dir should be normalized)"
        while True:
            (min_dist, closest) = self.scene.min_dist(pos)
            if min_dist > 1e3:
                # Assume way past edge of scene
                return self.sky
            if min_dist < 1e-3:
                return closest.material.albedo
            pos = pos + dir * min_dist

    def cast_ray_from_camera(self, xfrac, yfrac):
        # TODO optimize further?
        nxfrac = 1 - xfrac
        nyfrac = 1 - yfrac
        # Note: We flip the y axis because our y goes up, but Pillow y axis goes down
        coeff = np.array([
            nxfrac * yfrac,
            nxfrac * nyfrac,
            xfrac * yfrac,
            xfrac * nyfrac,
        ])
        return normalize(np.matmul(coeff, self.camera_edgeray_matrix))

    def draw_image(self):
        for x in range(self.width):
            for y in range(self.height):
                self.bitmap_data[y, x][:] = self.calc_pixel(x, y)
        return self.bitmap_data

if __name__ == '__main__':
    print("Running tests")
    assert(FEQ(dist(calc_edge_rays(1)[0], (-1, 1, -1)), 0))
    assert(FEQ(dist(calc_edge_rays(2)[0], (-1, 1, -2)), 0))
    renderer = Renderer(16, 16)
    assert(FEQ(dist(renderer.cast_ray_from_camera(0.5, 0.5), (0, 1, 0)), 0))
    # Evenly interpolating the 4 should give the y axis basis
    assert(FEQ(length(np.matmul([.25, .25, .25, .25], make_edgeray_matrix(calc_edge_rays(2)))), 1))
    print("All tests passed")
