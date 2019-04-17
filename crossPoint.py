class Point:
    x: float = 0
    y: float = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return (self.x == other.x 
            and self.y == other.y)
    def __hash__(self):
        return hash(self.x + self.y)
    def __str__(self):
        return f'{self.x} {self.y}'

class Side:
    side_from: Point = None
    side_to: Point = None

    def __init__(self, f: Point, t: Point):
        self.side_from = f
        self.side_to = t
    def __eq__(self, other):
        return (self.side_from == other.side_from 
            and self.side_to == other.side_to)
    def __str__(self):
        return f'from:{self.side_from}, to:{self.side_to}'


import numpy as np
import itertools as it

# 辺を２つ受け取り交差地点を計算する
#
# return 交差地点
def calc_cross_point(side1: Side, side2: Side) -> Point:
    # 交差地点計算
    Q1: Point = side1.side_to
    Q2: Point = side2.side_to
    P1: Point = side1.side_from
    P2: Point = side2.side_from
    mat_A = np.matrix([
        [Q1.x - P1.x, -(Q2.x - P2.x)], 
        [Q1.y - P1.y, -(Q2.y - P2.y)]
      ])
    A = np.linalg.det(mat_A) # 行列式

    mat = np.matrix([[P2.y - Q2.y, Q2.x - P2.x], [P1.y - Q1.y, Q1.x - P1.x]])
    _mat = np.matrix([[P2.x - P1.x], [P2.y - P1.y]])
    result = ((mat * _mat) / A).A1 # 問題中のs,tの計算, matrix -> arrayに変換

    # s, t が共に0 <= s,t <= 1.0の場合は交差地点があると判断し作成
    if all(tmp > 0 and tmp < 1 for tmp in result):
        s = result[0]
        x = round(P1.x + (Q1.x - P1.x) * s, 5)
        y = round(P1.y + (Q1.y - P1.y) * s, 5)
        return Point(x, y)

    # 交差地点がない場合Noneを返す
    return None

# 交差地点を列挙
#
# return 交差点(第1ソート:x, 第2ソート:y)
def list_cross_point(sides: [Side]) -> [Point]:
    cross_points: [Point] = []
    # print(list(map(lambda x: str(x), list(it.product(sides, sides))[-2])))
    for com in it.product(sides, sides):
        if is_cross_at_edge(com[0], com[1]):
            continue
        cross_point = calc_cross_point(com[0], com[1])
        if cross_point is not None:
            cross_points.append(cross_point)
    # print(list(map(lambda x: str(x), cross_points))[-2])

    return sorted(list(set(cross_points)), key = lambda point: (point.x, point.y))

# 2つの辺が端で交わっているか判断
def is_cross_at_edge(side1: Side, side2: Side) -> bool:
    return (side1.side_from == side2.side_from 
        or side1.side_to == side2.side_to
        or side1.side_from == side2.side_to
        or side1.side_to == side2.side_from)
