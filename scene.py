from imports import *
from vec import *

class Scene:
    def __init__(self):
        self.spheres = []
        self._prepared = False
        self._sphere_centers = None

    def add_object(self, obj):
        self._prepared = False
        match type(obj):
            case Sphere:
                self.spheres.append(obj)

    def _prepare(self):
        self._sphere_centers = np.concatenate([s.position for s in self.spheres])
        self._sphere_centers = self._sphere_centers.reshape((-1, 3))
        self._sphere_radii = np.array([s.radius for s in self.spheres])
        self._prepared = True

    def min_dist(self, pos):
        "Min signed dist from position to a surface in the scene + closest object"
        if not self._prepared:
            self._prepare()
        delta2s = (pos - self._sphere_centers) ** 2
        sdists = np.matmul(delta2s, c_one3) ** .5 - self._sphere_radii
        i = np.argmin(sdists)
        return (sdists[i], self.spheres[i])
