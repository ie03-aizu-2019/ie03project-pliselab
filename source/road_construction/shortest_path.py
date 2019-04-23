from typing import List, Dict, Optional
import math

from . import Side, Point, list_cross_point

def decide_shortest_path(from_id: str, to_id: str,
    graph: Dict[str, Dict[str, float]], n: int = 1) -> List[List[Point]]:
    """最短経路を求めます。

    Args:
        from_id (str): 開始地点ID。
        to_id (str): 目的地点ID。
        graph (Dict[str, Dict[str, float]]): 重み付きグラフ
        n (int, optional): いくつの経路を求めるか。 Defaults to 1.

    Returns:
        List[List[Point]]: 最短経路。n個の経路のリスト。
    """

    ids = list(graph.keys())
    # from, toのどちらかがNoneなら、経路を探索せずに終了
    if (from_id not in ids or to_id not in ids):
        return [[] for i in range(n)]




def struct_graph(sides, points: List[Point], cross_points: List[Point]) -> Dict[str, Dict[str, float]]:
    """重み付きグラフの構築

    Args:
        sides (List[Side]): 辺の一覧。
        points (List[Point]): 端点の一覧。
        cross_points (List[Point]): 交差地点の一覧。

    Returns:
        Dict[str, Dict[str, float]]: 重み付きグラフ
    """
    # id -> Pointの辞書を作成
    point_dict = dict(zip([str(i + 1) for i in range(len(points))], points))
    cross_point_dict = dict(zip(['C' + str(i + 1) for i in range(len(cross_points))], cross_points))
    all_point_dict = {**point_dict, **cross_point_dict}

    all_point_dic_inv = {v:k for k, v in all_point_dict.items()}

    ids = list(all_point_dic_inv.values())

    # 距離をinfで初期化
    g = {id1 : {id2 : math.inf for id2 in ids} for id1 in ids}

    # 距離情報を追加
    for s in sides:
        sp = s.points
        for i in range(len(s.points) - 1):
            d = sp[i].calc_distance(sp[i + 1])
            pid1 = all_point_dic_inv[sp[i]]
            pid2 = all_point_dic_inv[sp[i + 1]]
            g[pid1][pid2] = g[pid2][pid1] = d

    return g
