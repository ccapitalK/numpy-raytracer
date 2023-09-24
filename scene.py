from imports import *
from vec import *
from objects import *

GROUND_Z = -5

class Scene:
    def __init__(self, ground_material):
        self.spheres = []
        self._prepared = False
        self._sphere_centers = None
        self._ground = Ground(ground_material)
        self.light_position = np.array([0, 0, 2])
        self.light_dir = normalize(self.light_position)

    def add_object(self, obj):
        self._prepared = False
        match type(obj):
            case Sphere:
                self.spheres.append(obj)

    def set_light(self, pos):
        self.light_position = np.array(pos)
        self.light_dir = normalize(self.light_position)

    def get_light_dir(self, pos):
        return normalize(self.light_position-pos)

    def _prepare(self):
        self._sphere_centers = np.concatenate([s.position for s in self.spheres])
        self._sphere_centers = self._sphere_centers.reshape((-1, 3))
        self._sphere_radii = np.array([s.radius for s in self.spheres])
        self._prepared = True

    # Note: dir passed in to enable some opts
    def min_dist(self, pos, dir):
        "Min signed dist from position to a surface in the scene + closest object"
        if not self._prepared:
            self._prepare()
        delta2s = (pos - self._sphere_centers) ** 2
        signed_dists = np.matmul(delta2s, c_one3) ** .5 - self._sphere_radii
        i = np.argmin(signed_dists)
        # Hardcoded ground halfplane
        gdist = pos[2] - GROUND_Z
        if dir[2] < 0:
            # Dist to the ground point it would intersect at
            gdist = (GROUND_Z - pos[2]) / dir[2]
            if gdist < signed_dists[i]:
                return gdist, self._ground
        return signed_dists[i], self.spheres[i]
