from typing import List
from . import Side, Point, list_cross_point
import math


def calc_distance(side: Side, point: Point) -> float:
    """
    与えられた点と線分との距離を計算します。
    https://mathtrain.jp/tentotyokusen
    これのdの式のままにやる たぶんうまくいってない

    Args:
        side (Side): 線分
        point (Point): 座標

    Returns:
        線分と座標の間の最短距離
    """
    a = ((side.side_from.y - side.side_to.y) / (side.side_from.x - side.side_to.x))
    b = -1
    c = -a * side.side_to.x + side.side_to.y

    d = abs(a * point.x + b * point.y + c) / math.sqrt(a**2 + b**2)
    return d

def calc_distance_vec(side: Side, point: Point) -> float:
    """
    与えられた点と線分との距離を計算します。
    ベクトルでの計算ver

    Args:
        side (Side): 線分
        point (Point): 座標

    Returns:
        線分と座標の間の最短距離
    """

    # ベクトル
    vecA = (side.side_to.x - side.side_from.x, side.side_to.y - side.side_from.y)
    vecB = (point.x - side.side_from.x, point.y - side.side_from.y)

    # 内積
    inner = vecA[0] * vecB[0] + vecA[1] * vecB[1]
    print("side", side)
    print("point", point)
    print("vecA", vecA)
    print("vecB", vecB)
    print("inner", inner)
    print()

    # 距離
    distance = inner / (vecA[0] * vecA[0] + vecA[1] * vecA[1])
    return distance

def suggest_optional_road(sides: List[Side], point: Point) -> Point:
    """
    与えられた座標から道の提案をします。

    Args:
        sides (List[Side]): 全ての辺
        point (Point): 座標

    Returns:
        最適な道 に繋いだ時の交差地点の座標
    """

    cross_point: Point

    # 線分と座標との距離が一番近いものを取得
    min_distance_side = None
    min_distance = None
    for side in sides:
        d = calc_distance_vec(side, point)
        print(d)
        if min_distance is None or min_distance > d:
            min_distance = d
            min_distance_side = side
    print("最短距離の線分", min_distance_side)
    if min_distance <= 0.0:
        cross_point = min_distance_side.side_to
    elif min_distance >= 1:
        cross_point = min_distance_side.side_from
    else:
        x = min_distance_side.side_from.x + min_distance * (min_distance_side.side_to.x - min_distance_side.side_from.x)
        y = min_distance_side.side_from.y + min_distance * (min_distance_side.side_to.y - min_distance_side.side_from.y)
        cross_point = Point(x, y)

    sides += [Side(cross_point, point)]
    return cross_point
    
