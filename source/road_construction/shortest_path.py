from typing import List, Optional

from . import Side, Point, list_cross_point

def decide_shortest_path(
    from_id: str,
    to_id: str,
    sides: List[Side],
    points: List[Point],
    cross_points: List[Point],
    n: int = 1
    ) -> List[List[Point]]:
    """最短経路を求めます。

    Args:
        from_p (Optional[Point]): 開始地点。
        to_p (Optional[Point]): 目的地点。
        sides (List[Side]): 辺の一覧。
        points (List[Point]): 端点の一覧。
        cross_points (List[Point]): 交差地点の一覧。
        n (int, optional): 幾つの経路を求めるか。 Defaults to 1.

    Returns:
        List[List[Point]]: 最短経路。n個の経路のリスト。
    """

    point_dic = dict(zip([str(i + 1) for i in range(len(points))], points))
    cross_point_dic = dict(zip(['C' + str(i + 1) for i in range(len(cross_points))], cross_points))

    from_p = point_dic[from_id] if from_id in point_dic else cross_point_dic[from_id] if from_id in cross_point_dic else None
    to_p = point_dic[to_id] if to_id in point_dic else cross_point_dic[to_id] if to_id in cross_point_dic else None
    # from, toのどちらかがNoneなら、経路を探索せずに終了
    if (not from_p or not to_p):
        return [[] for i in range(n)]

    point_dic_inv = {v:k for k, v in point_dic.items()}
    side_ids = [(point_dic_inv[s.side_from], point_dic_inv[s.side_to]) for s in sides]

    print(side_ids)

    # TODO nについては考慮せずに、のちに実装する
    # print(from_p, to_p, [str(s) for s in sides])


def create_graph(points):
    pass