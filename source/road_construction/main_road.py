from typing import List
from pprint import pprint
from . import Side, Point, list_cross_point, build_graph
import json

def main_road():
    
    return

def connected_road(points: [Point], sides: [Side]):
    
    return

def find_bridge(sides: List[Side], points: List[Point], cross_points: List[Point]):
    """深さ優先探索をし、行きがけ順の番号、最小の行きがけ順を返す

    Args:
        sides (List[Side]): 辺の一覧
        points (List[Point]): 頂点の一覧
        cross_points (List[Point]): 交点の一覧
    Returns:
        List[(Point, int, int)]: 深さ優先探索後の頂点リスト Tuple: (頂点, 行きがけ順, 行きがけ順の最小)
    """

    # Dict[]
    stack: [Dict[str, str]] = []
    graph: Dict[str, Dict[str, float]] = build_graph(sides, points, cross_points)
    _graph: List[(str, str)] = []
    for k, v in graph.items():
        for key, val in v.items():
            _graph.append((k, key))

    # Dict[point ID, pre_order, min] 頂点と行きがけ順のDict作成, 行きがけ順を0で初期化
    points_pre_order = {key: {"pre" : None, "min" : None} for key, val in graph.items()}
    print(points_pre_order)
    print(depth_first_search(points_pre_order, list(points_pre_order.keys())[0], 0, _graph))

def depth_first_search(points: {str: {"pre":int, "min":int}}, id: str, pre: int, _graph) -> {str: {"pre":int, "min":int}}:
    # 全てのpreが埋まっていたら処理終了
    if all(map(lambda v: v["pre"], points.values())):
        print("end")
        return points
    points[id]["pre"] = pre

    # idの頂点に接続している辺を取得する(id)
    connected_points = map(lambda tup: tup[1], filter(lambda tup: tup[0] == id, _graph))

    for side in connected_points:
        if points[side]["pre"] is None:
            print("if")
            return depth_first_search(points, side, pre + 1, _graph)