from typing import List, Dict, Tuple, Optional

import math
from heapq import heappop, heappush

from . import Side, Point, list_cross_point

def decide_shortest_path(s: str, g: str,
    V: Dict[str, Dict[str, float]], n: int = 1) -> Tuple[float, List[str]]:
    """最短経路を求めます。

    Args:
        s (str): 開始地点ID。
        g (str): 目的地点ID。
        V (Dict[str, Dict[str, float]]): 重み付きグラフ
        n (int, optional): いくつの経路を求めるか。 Defaults to 1.

    Returns:
        Tuple[float, List[str]]: 最短経路の距離と経路。
    """

    ids = list(V.keys())
    # from, toのどちらかがNoneなら、経路を探索せずに終了
    if (s not in ids or g not in ids):
        return (None, None)

    dist = {id: math.inf for id in ids}
    prev = {id: None for id in ids}

    dist[s] = 0

    que = []
    heappush(que, (dist[s], s))

    while que:
        # 優先度が最小であるキューを取り出す
        dist_u, u = heappop(que)
        if dist[u] < dist_u:
            continue
        for p, d in V[u].items():
            if dist[p] > dist_u + d:
                dist[p] = dist_u + d
                prev[p] = u
                heappush(que, (dist[p], p))

    path = []
    n = g
    while n is not None:
        path.insert(0, n)
        n = prev[n]

    return (dist[g], path)


def struct_graph(sides, points: List[Point], cross_points: List[Point]) -> Dict[str, Dict[str, float]]:
    """重み付きグラフの構築。事前にlist_cross_pointを実行する必要あり。

    Args:
        sides (List[Side]): 辺の一覧。
        points (List[Point]): 端点の一覧。
        cross_points (List[Point]): 交差地点の一覧。

    Returns:
        Dict[str, Dict[str, float]]: 重み付きグラフ。地点ID1->地点ID2->距離。
    """
    # id -> Pointの辞書を作成
    point_dict = dict(zip([str(i + 1) for i in range(len(points))], points))
    cross_point_dict = dict(zip(['C' + str(i + 1) for i in range(len(cross_points))], cross_points))
    all_point_dict = {**point_dict, **cross_point_dict}
    # Point -> idの辞書を作成
    all_point_dic_inv = {v: k for k, v in all_point_dict.items()}

    ids = list(all_point_dic_inv.values())
    # 距離をinfで初期化
    V = {id1 : {id2: math.inf for id2 in ids} for id1 in ids}

    # 距離情報を追加
    for s in sides:
        sp = s.points
        for i in range(len(s.points) - 1):
            d = sp[i].calc_distance(sp[i + 1])
            pid1 = all_point_dic_inv[sp[i]]
            pid2 = all_point_dic_inv[sp[i + 1]]
            V[pid1][pid2] = V[pid2][pid1] = d

    return V
