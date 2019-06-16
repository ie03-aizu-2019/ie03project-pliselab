from typing import List, Set, Tuple, Optional

import os
import argparse
import random
import matplotlib.pyplot as plt

from road_construction import Point, Side
import road_construction as rc

X_Y_MAX = 8
K_MAX = 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n')
    parser.add_argument('-m')
    parser.add_argument('-p')
    parser.add_argument('-q')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    N = decide_input_num(args.n or '', 2, 200)
    M = decide_input_num(args.m or '', 1, N - 1)
    if (N <= M):
        M = N - 1
    P = decide_input_num(args.p or '', 0, 100)
    Q = decide_input_num(args.q or '', 0, 100)

    # 端点の列挙
    points_set: Set[Tuple[int, int]] = set()
    while len(points_set) < N:
        x = random.randint(0, X_Y_MAX)
        y = random.randint(0, X_Y_MAX)
        points_set.add((x, y))

    points: List[Point] = [Point(x, y) for x, y in points_set]

    # 辺の列挙
    side_from_to_set: Set[Tuple[int, int]] = set()
    while len(side_from_to_set) < M:
        fr = random.randint(0, N - 1)
        to = random.randint(0, N - 1)
        if fr != to and not (fr, to) in side_from_to_set:
            side_from_to_set.add((fr, to))

    sides: List[Side] = [Side(points[fr], points[to])
                         for fr, to in side_from_to_set]

    # 交差地点の列挙
    cross_points = rc.list_cross_point(sides)

    # 追加点の列挙
    add_points_set: Set[Tuple[int, int]] = set()
    while len(add_points_set) < P:
        x = random.randint(0, X_Y_MAX)
        y = random.randint(0, X_Y_MAX)
        if Point(x, y) not in points_set:
            add_points_set.add((x, y))

    add_points: List[Point] = [Point(x, y) for x, y in add_points_set]

    # 探索経路
    point_from_to_set: Set[Tuple[str, str, int]] = set()
    point_ids = [str(i + 1) for i in range(0, N)] + ['C' + str(i + 1)
                                                     for i in range(0, len(cross_points))]
    while len(point_from_to_set) < Q:
        fr = random.randint(0, len(point_ids) - 1)
        to = random.randint(0, len(point_ids) - 1)
        k = random.randint(1, K_MAX)
        if fr != to and (fr, to) not in [(f, t) for f, t, _k in point_from_to_set]:
            point_from_to_set.add((point_ids[fr], point_ids[to], k))

    # データの作成
    create_graph(points, cross_points, sides, add_points)
    data = create_test_data(N, M, P, Q,
                            points, list(side_from_to_set), add_points, list(point_from_to_set))
    if args.output:
        os.makedirs(args.output, exist_ok=True)
        os.chdir(args.output)
        with open('input.txt', 'w') as f:
            f.write(data)
        plt.savefig('figure.png')
    else:
        print(data)
        plt.show()


def decide_input_num(arg, bottom=0, top=0):
    """入力数を返します

    Args:
        arg (str): 数字、もしくは範囲 e.g. '1', '10', '1,100'
        bottom (Optional[int]): 範囲の下限. Defaults to 0.
        top (Optional[int]): 範囲の上限. Defaults to 0.

    Returns:
        int: 入力数
    """
    range = arg.split(',') if arg != '' else []
    if len(range) == 0:
        return random.randint(bottom, top)
    elif len(range) == 1:
        return int(range[0])
    else:
        return random.randint(*map(int, range))


def create_test_data(N, M, P, Q, points, from_to_sides, add_points, from_to_points):
    """入力データを作成します

    Args:
        N (int): N
        M (int): M
        P (int): P
        Q (int): Q
        points (List[Point]): 端点の一覧
        from_to_sides (List[Tuple[int, int]]): 辺の一覧(from, to)
        add_points (List[Point]): 追加点の一覧
        from_to_points (List[Tuple[str, str, int]]): 探索経路の一覧(from, to, k)
    """
    data = [f'{N} {M} {P} {Q}']
    data += [f'{int(p.x)} {int(p.y)}' for p in points]
    data += [f'{fr} {to}' for fr, to in from_to_sides]
    data += [f'{int(ap.x)} {int(ap.y)}' for ap in add_points]
    data += [f'{fr} {to} {k}' for fr, to, k in from_to_points]
    return '\n'.join(data)


def create_graph(points, cross_points, sides, add_points):
    """グラフを作成します

    Args:
        point (List[Point]): 端点の一覧
        cross_point (List[Point]): 交差点の一覧
        sides (List[Side]): 辺の一覧
        add_points (List[Point]): 追加点の一覧
    """
    for i, p in enumerate(points):
        plt.plot(p.x, p.y, 'ro', color='r')
        plt.text(p.x, p.y, i + 1, ha='center', va='bottom')

    for i, cp in enumerate(cross_points):
        plt.plot(cp.x, cp.y, 'ro', color='y')
        plt.text(cp.x, cp.y, f'C{i + 1}', ha='center', va='bottom')

    for s in sides:
        plt.plot([s.side_from.x, s.side_to.x], [s.side_from.y, s.side_to.y])

    for i, ap in enumerate(add_points):
        plt.plot(ap.x, ap.y, 'ro', color='b')
        plt.text(ap.x, ap.y, f'A{i + 1}', ha='center', va='bottom')

    plt.xlim(-1, X_Y_MAX + 1)
    plt.ylim(-1, X_Y_MAX + 1)
    plt.xlabel('X')
    plt.ylabel('Y')


if __name__ == "__main__":
    main()
