from pathlib import Path
from queue import PriorityQueue
from typing import Optional

from aoc import DATA
from aoc.common.executor import Executor

Coord = tuple[int, int]
Map = list[list[chr]]

def read_input(file: Path) -> tuple[Map, Coord]:
    data = open(file, "r").read()

    map_: Map = [[c for c in s] for s in data.split()]

    s_idx = data.index('S')
    # add plus 1 to consider for \n
    l = len(map_[0]) + 1
    start = (s_idx % l, s_idx // l)

    return map_, start

def part_one(file: Path):
    map_, start = read_input(file)

    open_ = PriorityQueue()
    open_.put((0, start, (1, 0)))
    closed = dict()

    cross = [
        (1, 0, 0, 1),
        (0, 1, -1, 0),
        (0, -1, 1, 0),
    ]

    while not open_.empty():
        cost, (x, y), (xv, yv) = open_.get_nowait()

        if map_[y][x] == 'E':
            return cost

        if (x, y) in closed:
            if cost >= closed[(x, y)]:
                continue

        closed[(x,y)] = cost

        for (a, b, c, d) in cross:
            xvn, yvn = xv * a + yv * b, xv * c + yv * d
            xn, yn = x + xvn, y+ yvn

            if (xn, yn) in closed:
                continue

            if map_[yn][xn] == '#':
                continue

            cn = cost + 1 + int((xv, yv) != (xvn, yvn)) * 1000

            open_.put_nowait(
                (cn, (xn, yn), (xvn, yvn))
            )

    return None

def reverse(x: int, y: int, cost: int, costs: dict[Coord, int], end: Coord):

    cross = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    tiles = {(x,y)}

    for (xv, yv) in cross:
        xn, yn = x+xv, y+yv

        if (xn, yn) not in costs:
            continue

        if costs[(xn, yn)] >= cost:
            continue

        reverse_rec(xn, yn, xv, yv, costs[(xn, yn)], costs, end, tiles)

    return tiles

def reverse_rec(x: int, y: int, xv: int, yv: int, cost: int, costs: dict[Coord, int], end: Coord, tiles: set[Coord]):

    tiles.add((x,y))

    if (x,y) == end:
        return

    cross = [
        (1, 0, 0, 1),
        (0, 1, -1, 0),
        (0, -1, 1, 0),
    ]

    for (a, b, c, d) in cross:
        xvn, yvn = xv * a + yv * b, xv * c + yv * d
        xn, yn = x + xvn, y + yvn

        if (xn, yn) not in costs:
            continue

        if costs[(xn, yn)] >= cost + int((xv, yv) == (xvn, yvn)) * 1000:
            continue

        reverse_rec(xn, yn, xvn, yvn, costs[(xn, yn)], costs, end, tiles)

def part_two(file: Path):
    map_, start = read_input(file)

    open_ = PriorityQueue()
    open_.put((0, start, (1, 0)))
    closed = dict()

    cross = [
        (1, 0, 0, 1),
        (0, 1, -1, 0),
        (0, -1, 1, 0),
    ]

    end: Optional[Coord] = None
    while not open_.empty():
        cost, (x, y), (xv, yv) = open_.get_nowait()

        if map_[y][x] == 'E':
            end = (x, y)

        if (x, y) in closed:
            if cost >= closed[(x, y)]:
                continue

        closed[(x, y)] = cost

        for (a, b, c, d) in cross:
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

    ex, ey = end
    tiles = reverse(ex, ey, closed[end], closed, start)

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