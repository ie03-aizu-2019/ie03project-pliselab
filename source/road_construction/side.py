from typing import List

from . import Point


class Side:
    side_from: Point
    side_to: Point
    points: List[Point]

    def __init__(self, f: Point, t: Point):
        self.side_from = f
        self.side_to = t
        self.points = [f, t]

    def __eq__(self, other):
        return self.side_from == other.side_from and self.side_to == other.side_to

    def __str__(self):
        return f'from:{self.side_from}, to:{self.side_to}'

    def add_point(self, point):
        dist = self.side_from.calc_distance(point)
        for i, p in enumerate(self.points):
            if dist < self.side_from.calc_distance(p) and point not in self.points:
                self.points.insert(i, point)
                break
