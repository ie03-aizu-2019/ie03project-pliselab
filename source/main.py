from typing import List, Optional

from road_construction import Point, Side, calc_cross_point, list_cross_point, decide_shortest_path

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
sides: List[Side] = [Side(points[f - 1], points[t - 1]) for f, t in [map(int, input().split()) for i in range(M)]]

# 交差地点の列挙
cross_points = list_cross_point(sides)
# for point in cross_points:
#     print(f'{point.x} {point.y}')

for i in range(P):
    input()

# 経路の列挙
for i in range(M):
    f_id, t_id, n = input().split()
    decide_shortest_path(f_id, t_id, sides, points, cross_points)