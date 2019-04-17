from cross_point import Point
from cross_point import Side
from cross_point import calc_cross_point
from cross_point import list_cross_point

# input
input_nums = list(map(int, input().split()))
# if len(input_nums) != 4:

N, M, P, Q = input_nums
points = []
for i in range(N):
    x, y = map(int, input().split())
    points.append(Point(x, y))

sides: [Side] = []
for i in range(M):
    fr, to = map(int, input().split())
    sides.append(Side(points[fr - 1], points[to - 1]))

cross_points = list_cross_point(sides)
for point in cross_points:
    print(f'{point.x} {point.y}')