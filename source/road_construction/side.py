from . import Point

class Side:
    side_from: Point
    side_to: Point

    def __init__(self, f: Point, t: Point):
        self.side_from = f
        self.side_to = t

    def __eq__(self, other):
        return self.side_from == other.side_from and self.side_to == other.side_to

    def __str__(self):
        return f'from:{self.side_from}, to:{self.side_to}'