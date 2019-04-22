from typing import List, Optional

from road_construction import Point, Side, calc_cross_point, list_cross_point

# input
input_nums = list(map(int, input().split()))

N, M, P, Q = input_nums
points: List[Point] = []
for i in range(N):
    x, y = map(int, input().split())
    points.append(Point(x, y))

sides: List[Side] = []
for i in range(M):
    fr, to = map(int, input().split())
    sides.append(Side(points[fr - 1], points[to - 1]))

cross_points = list_cross_point(sides)
for point in cross_points:
    print(f'{point.x} {point.y}')