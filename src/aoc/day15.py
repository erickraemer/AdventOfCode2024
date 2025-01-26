from pathlib import Path

from aoc import DATA
from aoc.common.executor import Executor

Coord = tuple[int, int]
Map = list[list[chr]]

MOVE_MAP = {
    '<': (-1, 0),
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1)
}

def read_input(file: Path) -> tuple[Map, Coord, str]:
    data = open(file, "r").read()

    map_, movement = data.split("\n\n")

    map_ = [[c for c in s] for s in map_.split()]
    movement = movement.replace("\n", "")

    def find_robot():
        for y in range(len(map_)):
            for x in range(len(map_[y])):
                if map_[y][x] == '@':
                    return x, y

    pos = find_robot()

    return map_, pos, movement


def shift(map_: Map, x: int, y: int, vx: int, vy: int) -> bool:
    """
    Shift 'O' boxes in (vx, vy) direction inplace if possible
    """
    c: chr = map_[y][x]

    if c == '#':
        return False

    if c == '.':
        return True

    xn, yn = x+vx, y+vy
    rec: bool = shift(map_, xn, yn, vx, vy)

    if rec:
        # swap
        map_[y][x], map_[yn][xn] =  map_[yn][xn], map_[y][x]

    return rec


def box_sum(map_: Map, c: chr) -> int:
    sum_ = 0
    for y in range(len(map_)):
        for x in range(len(map_[y])):
            if map_[y][x] == c:
                sum_ += 100 * y + x

    return sum_


def part_one(file: Path) -> int:
    map_, pos, movement = read_input(file)

    for m in movement:
        x, y = pos
        vx, vy = MOVE_MAP[m]
        xn, yn = x+vx, y+vy

        if map_[yn][xn] == '.':
            map_[y][x], map_[yn][xn] = map_[yn][xn], map_[y][x]

        elif map_[yn][xn] == 'O':
            if not shift(map_, x, y, vx, vy):
                continue

        else:
            continue

        pos = xn, yn

    sum_ = box_sum(map_, 'O')

    return sum_

def widen(map_: Map):
    """
    Widens the map inplace for part two
    """

    w_map = {
        '#': '#',
        'O': ']',
        '.': '.',
        '@': '.'
    }

    for l in map_:
        for i in range(len(l)):
            k: int = i * 2
            c: chr = l[k]

            if c == 'O':
                l[k] = '['

            l.insert(k + 1, w_map[c])

def shift_iter(map_: Map, x: int, y: int, vy: int):
    """
    Shift '[]' boxes in vy direction inplace along the y-axis if possible
    """
    open_ = [(x, y+vy)]
    closed = {(x,y): None}

    while open_:
        x, y = open_.pop(0)
        c = map_[y][x]

        if (x, y) in closed:
            continue

        if c == '#':
            return False

        if c == '.':
            continue

        xn, yn = x + (1 if map_[y][x] == '[' else -1), y + vy

        open_.append((x, yn))
        if map_[yn][x] != c:
            open_.append((xn, y+vy))

        # since python 3.7+ dicts keep the insertion order
        closed[(x, y)] = None
        closed[(xn, y)] = None

    for (x,y) in reversed(closed.keys()):
        # swap
        map_[y][x], map_[y + vy][x] = map_[y + vy][x], map_[y][x]

    return True


def part_two(file: Path):
    map_, pos, movement = read_input(file)

    widen(map_)
    # adjust position
    pos = pos[0] * 2, pos[1]

    brackets = {'[', ']'}

    for m in movement:
        x, y = pos
        vx, vy = MOVE_MAP[m]
        xn, yn = x + vx, y + vy

        if map_[yn][xn] == '.':
            map_[y][x], map_[yn][xn] = map_[yn][xn], map_[y][x]

        elif map_[yn][xn] in brackets:
            if vy == 0 and not shift(map_, x, y, vx, vy):
                continue

            if vx == 0 and not shift_iter(map_, x, y, vy):
                continue

        else:
            continue

        pos = xn, yn

    sum_ = box_sum(map_, '[')

    return sum_


def main():
    executor = Executor(
        test_file=DATA / "t15.txt",
        input_file=DATA / "i15.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(10092)
    executor.one("Box Score")

    executor.test_two(9021)
    executor.two("Box Score")


if __name__ == "__main__":
    main()