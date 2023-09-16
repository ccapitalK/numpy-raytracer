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
        # TODO
        self._sphere_centers = np.zeros((len(self.spheres), 3))
        self._prepared = True

    def min_dist(self, pos):
        "Min signed dist from position to a surface in the scene + closest object"
        if not self._prepared:
            self._prepare()
        min_dist, closest = m.inf, None
        for sphere in self.spheres:
            # TODO: Opt dist2
            curr_dist = dist(pos, sphere.position) - sphere.radius
            if curr_dist < min_dist:
                closest = sphere
                min_dist = curr_dist
        return (min_dist, closest)
