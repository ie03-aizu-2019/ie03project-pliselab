from typing import List
from . import Side, Point, list_cross_point
import math

def calc_distance(side: Side, point: Point) -> (float, Point):
    """
    与えられた点と線分との距離を計算します。
    ベクトルでの計算ver

    Args:
        side (Side): 線分
        point (Point): 座標

    Returns:
        線分と座標の間の最短距離, 最短距離の座標
    """

    # ベクトル
    vec = (side.side_to.x - side.side_from.x, side.side_to.y - side.side_from.y)
    tmp = float(-(vec[0] * (side.side_from.x - point.x) + vec[1] * (side.side_from.y - point.y))) / ((vec[0] ** 2) + (vec[1] ** 2))
    cross_point = None
    distance = 0.0

    if tmp < 0:
        cross_point = side.side_from
        distance = math.sqrt((cross_point.x - point.x) ** 2 + ((cross_point.y - point.y) ** 2))
    elif tmp > 1:
        cross_point = side.side_to
        distance = math.sqrt((cross_point.x - point.x) ** 2 + ((cross_point.y - point.y) ** 2))
    else:
        cross_point = Point(vec[0] * tmp + side.side_from.x, vec[1] * tmp + side.side_from.y)
        distance = math.sqrt((cross_point.x - point.x) ** 2 + ((cross_point.y - point.y) ** 2))
    return (float(distance), cross_point)

def suggest_optional_road(sides: List[Side], point: Point) -> Point:
    """
    与えられた座標から道の提案をします。

    Args:
        sides (List[Side]): 全ての辺
        point (Point): 座標

    Returns:
        最適な道 に繋いだ時の交差地点の座標
    """

    # 線分と座標との距離が一番近いものを取得
    min_distance_side = None
    min_distance = None
    min_side_cross_point = None
    for side in sides:
        dist, p = calc_distance(side, point)
        if min_distance is None or min_distance > abs(dist):
            min_distance = dist
            min_distance_side = side
            min_side_cross_point = p
    sides.append(Side(min_side_cross_point, point))
    
    return min_side_cross_point
    
