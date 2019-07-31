# -*- coding: utf-8 -*-

from typing import List, Optional

import argparse
import math
import matplotlib.pyplot as plt
import time

from road_construction import Point, Side
import road_construction as rc
import graph_generator as gg

# mode
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode')
args = parser.parse_args()
mode = args.mode or 'interactive'

mode_dict = {'5': '3', '6': '4', '9': 'interactive'}
if mode in mode_dict.keys():
    mode = mode_dict[mode]


def main():
    if mode == 'interactive':
        interactive()
    else:
        run()


def run():
    # input
    input_nums = list(map(int, input().split()))

    N, M, P, Q = input_nums

    # 端点の列挙
    # points: List[Point] = []
    # for i in range(N):
    #     x, y = map(int, input().split())
    #     points.append(Point(x, y))
    points: List[Point] = [Point(*(map(int, input().split())))
                           for i in range(N)]

    # 辺の列挙
    # sides: List[Side] = []
    # for i in range(M):
    #     fr, to = map(int, input().split())
    #     sides.append(Side(points[fr - 1], points[to - 1]))
    sides: List[Side] = [Side(points[f - 1], points[t - 1])
                         for f, t in [map(int, input().split()) for i in range(M)]]

    # 小課題1
    if mode == '1':
        is_cross, cross_point = rc.calc_cross_point(sides[0], sides[1])
        print(cross_point if is_cross else "NA")

    # 小課題2
    # 交差地点の列挙
    cross_points = rc.list_cross_point(sides)
    if mode == '2' or mode == 'all':
        print("cross points:")
        for point in cross_points:
            print(point)

    # 入力
    additional_points = []
    for i in range(P):
        additional_points.append(Point(*map(int, input().split())))

    # 経路の列挙
    V = rc.build_graph(sides, points, cross_points)
    # 小課題3,4,5,6
    for i in range(Q):
        f_id, t_id, k = input().split()
        if mode == '3' or mode == '4' or mode == 'all':
            print('decide shortest path')
            for dist, path in rc.decide_k_shortest_path(f_id, t_id, V, int(k)):
                print(f'{dist:.6g}' if dist != math.inf else "NA")
                if (mode == '4' or mode == 'all') and dist != math.inf:
                    print(' '.join(path))

    bridges = rc.find_bridge(sides, points, cross_points)

    # 小課題7
    if mode == '7' or mode == 'all':
        print('suggest new road:')
        for point in additional_points:
            res = rc.suggest_optional_road(sides, point)
            if res is not None:
                print(res)

    # 小課題8
    if mode == '8' or mode == 'all':
        print('main road')
        for road in bridges:
            if road["bridge_from"] is not None and road["bridge_to"] is not None:
                print(f'{road["bridge_from"]} {road["bridge_to"]}')


def interactive():
    points, sides, cross_points = [], [], []
    plot_flg = False
    while True:
        try:
            query_str = input(">>> ")
            query = query_str.split(' ')
            q = query[0]

            # 点の追加
            if q in ['add']:
                points.append(Point(int(query[1]), int(query[2])))
                print(f'add {len(points)}')

            # 辺の追加
            elif q in ['connect', 'con']:
                fr, to = int(query[1]) - 1, int(query[2]) - 1
                if fr == to:
                    print(f'Choose different points')
                    continue

                sides.append(Side(points[fr], points[to]))
                cross_points = rc.list_cross_point(sides)
                print(f'connect {fr + 1} and {to + 1}')

            # 点の追加・自動接続
            elif q in ['add-connect', 'add-con']:
                point1 = Point(int(query[1]), int(query[2]))
                point2 = rc.suggest_optional_road(sides, point1)
                for p in [point1, point2]:
                    if p not in points:
                        points.append(p)
                print(point2)
                cross_points = rc.list_cross_point(sides)

            # 一覧の表示
            elif q in ['list']:
                # 交差点
                if query[1] in ['crosspoint', 'cross']:
                    for point in cross_points:
                        print(point)
                # 橋(幹線道路)
                elif query[1] in ['bridge']:
                    for road in rc.find_bridge(sides, points, cross_points):
                        print(f'{road["bridge_from"]} {road["bridge_to"]}')

            # 経路探索
            elif q in ['search']:
                f_id, t_id = query[1], query[2]
                k = int(query[3]) if len(query) > 3 else 1

                V = rc.build_graph(sides, points, cross_points)
                for dist, path in rc.decide_k_shortest_path(f_id, t_id, V, k):
                    print(f'{dist:.6g}' if dist != math.inf else "NA")
                    if dist != math.inf:
                        print(' '.join(path))

            # グラフの表示
            elif q in ['plot']:
                # 終了
                if len(query) > 1 and query[1] in ['close']:
                    plt.close()
                    plot_flg = False
                # 表示開始
                else:
                    plot_flg = True

            # 終了
            elif q in ['quit', 'q', 'exit']:
                plt.close()
                break
            else:
                print(f'Illegal Query: {query_str}')

            # グラフの更新
            if plot_flg:
                plt.close()
                gg.create_graph(points, cross_points, sides, [],
                                max([p.x for p in points] + [p.y for p in points] + [0]))
                plt.show(block=False)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
