from typing import List, Optional

import numpy as np
import itertools as it

from . import Side, Point


def calc_cross_point(side1: Side, side2: Side) -> Optional[Point]:
    """辺を2つ受け取り交差地点を計算する。
    交差地点がない場合Noneを返す。

    Args:
        side1 (Side): 1つ目の辺。
        side2 (Side): 2つ目の辺。

    Returns:
        Optional[Point]: 交差地点。
    """
    # 交差地点計算
    Q1: Point = side1.side_to
    Q2: Point = side2.side_to
    P1: Point = side1.side_from
    P2: Point = side2.side_from
    mat_A = np.matrix([
        [Q1.x - P1.x, -(Q2.x - P2.x)],
        [Q1.y - P1.y, -(Q2.y - P2.y)]
    ])
    # 行列式
    A = np.linalg.det(mat_A)
    if (A == 0):
        return None

    mat = np.matrix([[P2.y - Q2.y, Q2.x - P2.x], [P1.y - Q1.y, Q1.x - P1.x]])
    _mat = np.matrix([[P2.x - P1.x], [P2.y - P1.y]])
    result = ((mat * _mat) / abs(A)).A1  # 問題中のs,tの計算, matrix -> arrayに変換

    # s, t が共に0 <= s,t <= 1.0の場合は交差地点があると判断し作成
    if all(tmp > 0 and tmp < 1 for tmp in result):
        s = result[0]
        x = round(P1.x + (Q1.x - P1.x) * s, 5)
        y = round(P1.y + (Q1.y - P1.y) * s, 5)
        return Point(x, y)

    # 交差地点がない場合Noneを返す
    return None


def list_cross_point(sides: List[Side]) -> List[Point]:
    """交差地点を列挙。辺に交差地点の情報を追加する。

    Args:
        sides (List[Side]): 辺の一覧。
    Returns:
        List[Point]: 交差点(第1ソート:x, 第2ソート:y)。
    """
    cross_points: [Point] = []

    for com in it.product(sides, sides):
        if is_cross_at_edge(com[0], com[1]):
            continue
        cross_point = calc_cross_point(com[0], com[1])
        if cross_point is not None:
            cross_points.append(cross_point)
            com[0].add_point(cross_point)

    return sorted(list(set(cross_points)), key=lambda point: (point.x, point.y))


def is_cross_at_edge(side1: Side, side2: Side) -> bool:
    """2つの辺が端で交わっているか判断。

    Args:
        side1 (Side): 1つ目の辺。
        side2 (Side): 2つ目の辺。

    Returns:
        bool: 2つの辺が端で交わっているか。
    """
    return (side1.side_from == side2.side_from
            or side1.side_to == side2.side_to
            or side1.side_from == side2.side_to
            or side1.side_to == side2.side_from)
