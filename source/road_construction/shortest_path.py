from typing import List, Dict, Tuple, Optional

import math
import copy
from heapq import heappop, heappush

from . import Side, Point, list_cross_point

from tabulate import tabulate


def _print_v(V):
    """グラフを表で出力"""
    table = [[k] + list(V[k].values()) for k in V.keys()]
    headers = V.keys()
    print(tabulate(table, headers, tablefmt="grid"))


def decide_k_shortest_path(s: str, g: str, V: Dict[str, Dict[str, float]], k: int) -> List[Tuple[float, List[str]]]:
    """K最短経路を求めます。

    Args:
        s (str): 開始地点ID。
        g (str): 目的地点ID。
        V (Dict[str, Dict[str, float]]): 重み付きグラフ
        k (int) 第何経路まで求めるか

    Returns:
        List[Tuple[float, List[str]]]: 第K経路までの距離と経路。
    """

    # 最短経路 (第1最短経路)
    result: List[Tuple[float, List[str]]] = [decide_shortest_path(s, g, V)]
    if result[0][0] is None or result[0][0] == math.inf:
        return result

    # 候補一覧
    candidate: List[Tuple[float, List[str]]] = []

    for n in range(k - 1):
        # 第{n + 2}最短経路
        _, path = result[n]

        # 候補を求める
        for super_node_idx, super_node in enumerate(path[:-1]):
            super_root = path[:super_node_idx]
            # 新規の重み付きグラフを作成
            v = copy.deepcopy(V)
            # 第{n + 1}経路以内の経路で使用した、super nodeからの道を削除する
            for _, p in result:
                if super_node in p:
                    i = p.index(super_node)
                    v[p[i]][p[i + 1]] = math.inf

            # 新規のグラフでのsuper root以降の最短経路を求める
            # 上で道を削除したことで、少し遠回りの道が最短経路になる
            _, p = decide_shortest_path(super_node, g, v)

            p = super_root + p
            # 元々のグラフを使用して距離を求める
            d = calc_path_distance(p, V)

            # 第K経路までに含まれていない、かつ、候補に存在しない場合、候補に追加
            # 同じ点を2回通るような経路は候補に入れない
            if not p in [r[1] for r in result] and not p in [c[1] for c in candidate] and len(p) == len(set(p)):
                heappush(candidate, (d, p))

        # 候補から距離が最小のものを取り出す
        if candidate:
            next = heappop(candidate)
            if next[0] == math.inf:
                break
            result.append(next)
        else:
            break

    return result


def calc_path_distance(path: List[str], V: Dict[str, Dict[str, float]]) -> float:
    """
    経路の距離を求めます

    Args:
        path (List[str]): 経路
        V (Dict[str, Dict[str, float]]): 重み付きグラフ
    Returns:
        float: 距離
    """
    if len(path) <= 1:
        return math.inf
    return sum([V[path[i]][path[i + 1]] for i in range(len(path) - 1)])


def decide_shortest_path(s: str, g: str, V: Dict[str, Dict[str, float]]) -> Tuple[float, List[str]]:
    """最短経路を求めます。(ダイクストラ法)

    Args:
        s (str): 開始地点ID。
        g (str): 目的地点ID。
        V (Dict[str, Dict[str, float]]): 重み付きグラフ

    Returns:
        Tuple[float, List[str]]: 最短経路の距離と経路。
    """

    ids = list(V.keys())
    # from, toのどちらかが不正なら、経路を探索せずに終了
    if (s not in ids or g not in ids):
        return (math.inf, [])

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
        # 必要なら -> for p, d in sorted(V[u].items(), lambda k, v: k):
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


def build_graph(sides, points: List[Point], cross_points: List[Point]) -> Dict[str, Dict[str, float]]:
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
    cross_point_dict = dict(
        zip(['C' + str(i + 1) for i in range(len(cross_points))], cross_points))
    all_point_dict = {**point_dict, **cross_point_dict}
    # Point -> idの辞書を作成
    all_point_dic_inv = {v: k for k, v in all_point_dict.items()}

    ids = list(all_point_dic_inv.values())
    # 距離をinfで初期化
    V = {id1: {id2: math.inf for id2 in ids} for id1 in ids}

    # 距離情報を追加
    for s in sides:
        sp = s.points
        for i in range(len(s.points) - 1):
            d = sp[i].calc_distance(sp[i + 1])
            pid1 = all_point_dic_inv[sp[i]]
            pid2 = all_point_dic_inv[sp[i + 1]]
            V[pid1][pid2] = V[pid2][pid1] = d

    return V
