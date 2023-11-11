#!/usr/bin/env python3

from imports import *
from vec import *
from objects import *
from scene import *

HFOV_DEGREES = 90
HFOV = (HFOV_DEGREES / 180) * m.pi
# Skew down
_CAMERA_SKEW = np.array([0, 0, -0.4])

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
        self.camera_edge_rays = [v + _CAMERA_SKEW for v in calc_edge_rays(height / width)]
        self.camera_edgeray_matrix = make_edgeray_matrix(self.camera_edge_rays)
        self.sky = c_zero3

    def set_sky_colors(self, colors):
        self.sky = colors

    def get_sky(self, pos):
        t = .5 - (np.dot(normalize(pos), self.scene.light_dir) * .5)
        return lerp(self.sky[0], self.sky[1], t)

    def calc_pixel(self, x, y):
        self.colour[1] = y / self.width
        ray = self.cast_ray_from_camera(x/self.width, y/self.height)
        return 255 * clip01(self.cast_ray(c_zero3.copy(), ray))

    def march_ray(self, pos, dir):
        """
        Cast ray from pos in dir (dir should be normalized)
        Returns: (distance, closest_object)
        """
        while True:
            min_dist, closest = self.scene.min_dist(pos, dir)
            if min_dist > 1e5:
                # Assume way past edge of scene
                return pos, None
            if min_dist < 1e-3:
                return pos, closest
            pos += dir * min_dist

    def cast_ray(self, pos, dir, depth=10):
        "Cast ray from pos in dir (dir should be normalized)"
        final_pos, closest = self.march_ray(pos, dir)
        if closest is None:
            return self.get_sky(final_pos)
        mat = closest.material
        norm = closest.get_norm(final_pos)
        obj_color = self.calc_incident_color(final_pos, dir, closest, norm)
        if FLEQ(mat.reflect, 0) or depth <= 1:
            return obj_color
        reflected = reflect(dir, norm)
        next = self.cast_ray(final_pos + reflected * 1e-3, reflected, depth-1)
        return lerp(obj_color, next, mat.reflect)

    def calc_incident_color(self, pos, dir, obj, norm):
        ndir = dir * -1
        light_dir = self.scene.get_light_dir(pos)
        diff = max(0, np.dot(norm, light_dir))
        spec = 0
        return obj.material.get_color(diff, spec)

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
    import material
    print("Running tests")
    assert(FEQ(dist(calc_edge_rays(1)[0], np.array((-1., 1., -1.))), 0.))
    assert(FEQ(dist(calc_edge_rays(2)[0], np.array((-1., 1., -2.))), 0.))
    scene = Scene(material.Material((0., 0., 0.)))
    renderer = Renderer(16, 16, scene)
    expected_center = normalize(np.array((0., 1., 0.)) + _CAMERA_SKEW)
    assert(FEQ(dist(renderer.cast_ray_from_camera(0.5, 0.5), expected_center), 0.))
    # Evenly interpolating the 4 should give the y axis basis
    assert(FEQ(length(np.matmul([.25, .25, .25, .25], make_edgeray_matrix(calc_edge_rays(2.)))), 1))
    print("All tests passed")
