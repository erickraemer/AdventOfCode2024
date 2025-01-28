from pathlib import Path
from queue import PriorityQueue
from typing import Final

from aoc import DATA
from aoc.common.executor import Executor

Coord = tuple[int, int]
Mat = tuple[int, int, int, int]
Map = list[list[chr]]

# Left, straight, right rotations matrices
LSR_ROT: Final[list[Mat]] = [
    (0, 1, -1, 0),  # turn left
    (1, 0, 0, 1),  # straight (identity)
    (0, -1, 1, 0),  # turn right
]

# cross offset values
CROSS: Final[list[Coord]] = [
    (0, 1),  # up
    (1, 0),  # right
    (0, -1),  # down
    (-1, 0)  # left
]


def read_input(file: Path) -> tuple[Map, Coord]:
    data = open(file, "r").read()

    map_: Map = [[c for c in s] for s in data.split()]

    s_idx = data.index('S')
    # add plus 1 to consider for \n
    l = len(map_[0]) + 1
    start = (s_idx % l, s_idx // l)

    return map_, start


def dijkstra(map_: Map, start: Coord):
    open_ = PriorityQueue()
    open_.put((0, start, (1, 0)))
    closed = dict()

    while not open_.empty():
        cost, (x, y), (xv, yv) = open_.get_nowait()

        if (x, y) in closed:
            if cost >= closed[(x, y)]:
                continue

        closed[(x, y)] = cost

        if map_[y][x] == 'E':
            return cost, (x, y), closed

        for (a, b, c, d) in LSR_ROT:
            xvn, yvn = xv * a + yv * b, xv * c + yv * d
            xn, yn = x + xvn, y + yvn

            if (xn, yn) in closed:
                continue

            if map_[yn][xn] == '#':
                continue

            cn = cost + 1 + int((xv, yv) != (xvn, yvn)) * 1000

            open_.put_nowait(
                (cn, (xn, yn), (xvn, yvn))
            )

    return None


def part_one(file: Path):
    cost = dijkstra(*read_input(file))[0]
    return cost


def walk_downhill_rec(x: int, y: int, xv: int, yv: int, costs: dict[Coord, int], end: Coord, tiles: set[Coord]):
    # constants: costs, end, tiles
    def rec(x_: int, y_: int, xv_: int, yv_: int):
        tiles.add((x_, y_))

        if (x_, y_) == end:
            return

        # Check straight, left and right turn
        for (a_, b_, c_, d_) in LSR_ROT:
            xvn_, yvn_ = xv_ * a_ + yv_ * b_, xv_ * c_ + yv_ * d_
            xn_, yn_ = x_ + xvn_, y_ + yvn_

            if (xn_, yn_) not in costs:
                continue

            cost_: int = costs[(x_, y_)]
            if (xv_, yv_) == (xvn_, yvn_):
                # ignore turn penalty on direction change
                cost_ += 1000

            if costs[(xn_, yn_)] >= cost_:
                continue

            rec(xn_, yn_, xvn_, yvn_)

    rec(x, y, xv, yv)


def walk_downhill(x: int, y: int, costs: dict[Coord, int], end: Coord):
    """
    Walk backwards from end to start, taking every path which monotonically decreases.
    """

    tiles = {(x, y)}

    # Check every direction
    for (xv, yv) in CROSS:
        xn, yn = x + xv, y + yv

        if (xn, yn) not in costs:
            continue

        if costs[(xn, yn)] >= costs[(x, y)]:
            continue

        walk_downhill_rec(xn, yn, xv, yv, costs, end, tiles)

    return tiles


def part_two(file: Path):
    map_, start = read_input(file)
    _, (x, y), costs = dijkstra(map_, start)
    tiles = walk_downhill(x, y, costs, start)

    return len(tiles)


def main():
    executor = Executor(
        test_file=DATA / "t16.txt",
        input_file=DATA / "i16.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(7036)
    executor.one("Shortest Path")

    executor.test_two(45)
    executor.two("Unique tiles")


if __name__ == "__main__":
    main()
