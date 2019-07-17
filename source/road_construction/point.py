import math

class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x + self.y)

    def __str__(self):
        return f'{round(self.x, 5)} {round(self.y, 5)}'

    def calc_distance(self, other) -> float:
        """対象の座標までの距離を求めます

        Args:
            other (Point): 対象の座標

        Returns:
            float: 距離
        """
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
    

