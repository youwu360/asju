import numpy as np


class RectangleRegion:

    # point -> (y, x)
    points = []

    def clear(self):
        self.points = []

    def add_point(self, point):
        self.points.append(list(point))

    def get_region(self):
        y0 = np.min(point[0] for point in self.points)
        y1 = np.max(point[0] for point in self.points)
        x0 = np.min(point[1] for point in self.points)
        x1 = np.max(point[1] for point in self.points)

        return [[y0, x0], [y1, x1]]

    def get_region_by_points(self, points):
        self.points = points
        return self.get_region()
