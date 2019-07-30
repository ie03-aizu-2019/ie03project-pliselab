from typing import List
from pprint import pprint
from collections import defaultdict
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

    # ある頂点から別の頂点への関係のみを持ったリスト
    _graph: Dict[str, List[str]] = defaultdict(lambda: [])
    for k, v in graph.items():
        for key, val in v.items():
            if val != float('inf'):
                _graph[k].append(key)

    # Dict[point ID, pre_order, min] 頂点と行きがけ順のDict作成, 行きがけ順, 最小値をinfで初期化
    points_pre_order = {key: {"pre" : float('inf'), "min" : float('inf'), "prev": None} for key, val in graph.items()}
    depth_first_search(points_pre_order, list(points_pre_order.keys())[0], 1, _graph)

def depth_first_search(points: {str: {"pre":int, "min":int, "prev": str}}, id: str, pre: int, _graph) -> [{"bridge_from": str, "bridge_to": str}]:
    """深さ優先探索をする。（行きがけ順、最小値を保存する）

    Args:
        points (Dict[str: {"pre":int, "min":int}]): グラフの頂点一覧。引数で渡ってきた際にはpre, minはinf
        id (str): 開始頂点ID。頂点IDは point のkey
        pre (int): 行きがけ順
        _graph (Dict[str, List[str]]): ある頂点から別の頂点への関係のみを持ったリスト

    """

    # 開始地点をスタックに積む
    initPlace = list(points.items())[0]
    stack = [initPlace]
    points[stack[0][0]]["pre"] = 0
    points[stack[0][0]]["min"] = 0

    bridges: [{"bridge_from": str, "bridge_to": str}] = []

    # スタックが空になったら終了
    while stack:
        # 現在地を取得
        current = stack[-1]
        nears = list(filter(lambda x : points[x]["pre"] == float('inf'), _graph[current[0]]))
        
        if nears:
            points[nears[0]]["pre"] = pre
            points[nears[0]]["min"] = pre
            points[nears[0]]["prev"] = current[0]
            pre += 1
            stack.append((nears[0], points[nears[0]]))
        else:
            adj = list(filter(lambda x : points[x]["pre"] != float('inf'), _graph[current[0]]))
            tmp = list(filter(lambda x : points[x]["pre"] != current[1]["pre"] - 1, adj))
            if tmp:
                tmp.sort(key=lambda x : points[x]["min"])
                points[current[0]]["min"] = points[tmp[0]]["min"]
            stack.pop()
    bridge_tos = list(filter(lambda x : x[1]["pre"] == x[1]["min"] and (x[1]["pre"] != initPlace[1]["pre"]), points.items()))

    for bridge_to in bridge_tos:
        bridges.append({"bridge_from": bridge_to[1]["prev"], "bridge_to": bridge_to[0]})
    return bridges