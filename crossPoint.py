class Point:
    x: float = 0
    y: float = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Side:
    side_from: Point = None
    side_to: Point = None

    def __init__(self, f: Point, t: Point):
        self.side_from = f
        self.side_to = t


import numpy as np

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
    if all(tmp >= 0 and tmp <= 1 for tmp in result):
        s = result[0]
        x = P1.x + (Q1.x - P1.x) * s
        y = P1.y + (Q1.y - P1.y) * s
        return Point(x, y)

    # 交差地点がない場合Noneを返す
    return None