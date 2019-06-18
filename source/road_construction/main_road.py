from typing import List
from pprint import pprint
from . import Side, Point, list_cross_point, struct_graph

def main_road():
    
    return

def connected_road(points: [Point], sides: [Side]):
    
    return

def dfs(sides: List[Side], points: List[Point], cross_points: List[Point]) -> [(Point, int, int)]:
    """

    """
    # Dict[fromID, toID]
    stack: [Dict[str, str]] = []
    graph: Dict[str, Dict[str, float]] = struct_graph(sides, points, cross_points)
    _graph: Dict[str, str] = []
    for dic in graph:
        for key in dic.keys():
            _graph[dic.key] = key

    # Tuple[Point, pre_order, min] 頂点と行きがけ順のDict作成, 行きがけ順を0で初期化
    points_pre_order: [(Point, int, int)] = [(point, 0, 0) for point in points]
    
    pprint(_graph)
