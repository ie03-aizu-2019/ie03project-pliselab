import os
import argparse
import matplotlib.pyplot as plt

from road_construction import Point, Side
import road_construction as rc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    # input
    input_nums = list(map(int, input().split()))

    N, M, P, Q = input_nums
    # 端点の列挙
    points: List[Point] = [Point(*(map(int, input().split())))
                           for i in range(N)]
    # 辺の列挙
    sides: List[Side] = [Side(points[f - 1], points[t - 1])
                         for f, t in [map(int, input().split()) for i in range(M)]]
    # 交差地点の列挙
    cross_points = rc.list_cross_point(sides)
    # 追加点の列挙
    add_points: List[Point] = [
        Point(*(map(int, input().split()))) for i in range(P)]
    for i in range(Q):
        input()

    all_points = points + add_points

    create_graph(points, cross_points, sides, add_points,
                 max([p.x for p in all_points] + [p.y for p in all_points]))

    if args.output:
        os.makedirs(args.output, exist_ok=True)
        os.chdir(args.output)
        plt.savefig('figure.png')
    else:
        plt.show()


def create_graph(points, cross_points, sides, add_points, x_y_max):
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

    plt.xlim(-1, x_y_max + 1)
    plt.ylim(-1, x_y_max + 1)
    plt.xlabel('X')
    plt.ylabel('Y')


if __name__ == "__main__":
    main()
