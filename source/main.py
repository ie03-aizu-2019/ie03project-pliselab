from typing import List, Optional

import argparse

from road_construction import Point, Side
import road_construction as rc

# mode
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode')
args = parser.parse_args()
mode = args.mode or "4"

# input
input_nums = list(map(int, input().split()))

N, M, P, Q = input_nums

# 端点の列挙
# points: List[Point] = []
# for i in range(N):
#     x, y = map(int, input().split())
#     points.append(Point(x, y))
points: List[Point] = [Point(*(map(int, input().split()))) for i in range(N)]

# 辺の列挙
# sides: List[Side] = []
# for i in range(M):
#     fr, to = map(int, input().split())
#     sides.append(Side(points[fr - 1], points[to - 1]))
sides: List[Side] = [Side(points[f - 1], points[t - 1])
                     for f, t in [map(int, input().split()) for i in range(M)]]

# 交差地点の列挙
cross_points = rc.list_cross_point(sides)
# 小課題1,2
if mode == '1' or mode == '2':
    for point in cross_points:
        print(f'{point.x} {point.y}')

for i in range(P):
    input()

# 経路の列挙
V = rc.struct_graph(sides, points, cross_points)
# 小課題3,4
if mode == '3' or mode == '4':
    for i in range(Q):
        f_id, t_id, n = input().split()
        dist, path = rc.decide_shortest_path(f_id, t_id, V)
        print('{:.5f}'.format(dist) if dist is not None else "NA")
        if mode == '4' and path is not None:
            print(' '.join(path))
