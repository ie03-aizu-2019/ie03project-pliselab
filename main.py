from crossPoint import Point
from crossPoint import Side
from crossPoint import calc_cross_point

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

if calc_cross_point(sides[0], sides[1]) == None:
    print('NA') 
else:
    print()

print(calc_cross_point(sides[0], sides[1]))