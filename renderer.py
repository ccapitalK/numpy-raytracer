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
    def __init__(self, width, height, scene):
        width = int(width)
        height = int(height)
        self.colour = np.zeros(3)
        self.bitmap_data = np.zeros((height, width, 3), dtype=np.uint8)
        self.width = width
        self.height = height
        self.scene = scene
        # Skew down
        skew = np.array([0, 0, 0.5])
        self.camera_edge_rays = [v - skew for v in calc_edge_rays(height / width)]
        self.camera_edgeray_matrix = make_edgeray_matrix(self.camera_edge_rays)
        self.sky = c_zero3

    def set_sky_color(self, color):
        self.sky = np.array(color)

    def calc_pixel(self, x, y):
        self.colour[1] = y / self.width
        ray = self.cast_ray_from_camera(x/self.width, y/self.height)
        return 255 * clip01(self.cast_ray(c_zero3.copy(), ray))

    def cast_ray(self, pos, dir, depth=6):
        "Cast ray from pos in dir (dir should be normalized)"
        while True:
            min_dist, closest = self.scene.min_dist(pos, dir)
            if min_dist > 1e5:
                # Assume way past edge of scene
                return self.sky
            if min_dist < 1e-3:
                mat = closest.material
                norm = closest.get_norm(pos)
                obj_color = self.calc_incident_color(pos, dir, closest, norm)
                if FLEQ(mat.reflect, 0) or depth <= 1:
                    return obj_color
                reflected = reflect(dir, norm)
                next = self.cast_ray(pos + reflected * 1e-3, reflected, depth-1)
                return lerp(obj_color, next, mat.reflect)
            pos += dir * min_dist

    def calc_incident_color(self, pos, dir, obj, norm):
        return obj.material.albedo

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
        for y in range(self.height):
            if y % 8 == 0:
                print(f"Scanline {y}/{self.height}")
            for x in range(self.width):
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
