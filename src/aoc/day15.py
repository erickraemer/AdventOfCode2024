from pathlib import Path

from aoc import DATA
from aoc.common.executor import Executor

Coord = tuple[int, int]

def read_input(file: Path) -> tuple[list[list[chr]], Coord, str]:
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

def walk(map_: list[list[chr]], x: int, y: int, vx: int, vy: int):
    """
    walk in a straight line until '#' or '.' is found and return the position
    """

    while True:
        x, y = x + vx, y + vy

        if map_[y][x] in {'#', '.'}:
            return x, y

def shift(map_: list[list[chr]], x1: int, y1: int, x2: int, y2: int, vx: int, vy: int):
    """
    Shift all characters of the map between (x1, y1) and (x2, y2) by one
    """

    if x1 > x2:
        x1, x2 = x2, x1

    if y1 > y2:
        y1, y2 = y2, y1

    buffer = [map_[y_][x_] for y_ in range(y1, y2+1) for x_ in range(x1, x2+1)]
    for i, c in enumerate(buffer):
        map_[y1 + (i + 1 * vy) % (y2 + 1 - y1)][x1 + (i + 1 * vx) % (x2 + 1 - x1)] = c

def box_sum(map_: list[list[chr]], c: chr):
    sum_ = 0
    for y in range(len(map_)):
        for x in range(len(map_[y])):
            if map_[y][x] == c:
                sum_ += 100 * y + x

    return sum_

def part_one(file: Path):
    map_, pos, movement = read_input(file)

    move_map = {
        '<': (-1, 0),
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1)
    }

    for m in movement:
        x, y = pos
        vx, vy = move_map[m]
        xn, yn = x+vx, y+vy

        if map_[yn][xn] == '#':
            continue

        if map_[yn][xn] == '.':
            map_[y][x], map_[yn][xn] = map_[yn][xn], map_[y][x]

        elif map_[yn][xn] == 'O':
            px, py = walk(map_, xn, yn, vx, vy)

            if map_[py][px] == '#':
                continue

            if map_[py][px] == '.':
                shift(map_, x,y,px,py,vx,vy)

        pos = xn, yn

    sum_ = box_sum(map_, 'O')

    return sum_

def widen(map_: list[list[chr]]):
    """
    Widens the map for part two
    """
    widened = []

    for l in map_:
        wl = []
        for c in l:

            if c == '#':
                wl.extend(['#', '#'])
            elif c == 'O':
                wl.extend(['[', ']'])
            elif c == '.':
                wl.extend(['.', '.'])
            elif c == '@':
                wl.extend(['@', '.'])
        widened.append(wl)

    return widened

def walk_rec(map_: list[list[chr]], x: int, y: int, vy: int):
    """
    Checks if boxes are moveable in the direction of vy on the y-axis
    :return True if moveable else False
    """

    c = map_[y][x]

    if c == '#':
        return False

    if c == '.':
        return True

    d = 1 if c == '[' else -1
    return all([
        walk_rec(map_, x, y+vy, vy),
        walk_rec(map_, x+d, y+vy, vy)
    ])

def shift_rec(map_: list[list[chr]], x: int, y: int, vy: int):
    """
    Recursively shifts all boxes in the direction of vy on the y-axis
    """

    def _rec(x_, y_):
        cn = map_[y_ + vy][x_]

        if cn != '.':
            shift_rec(map_, x_, y_ + vy, vy)

        map_[y_][x_], map_[y_ + vy][x_] = map_[y_ + vy][x_], map_[y_][x_]

    d = 1 if map_[y][x] == '[' else -1
    _rec(x, y)
    _rec(x+d, y)

def part_two(file: Path):
    map_, pos, movement = read_input(file)

    map_ = widen(map_)
    # adjust position
    pos = pos[0] * 2, pos[1]

    move_map = {
        '<': (-1, 0),
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1)
    }

    for m in movement:
        x, y = pos
        vx, vy = move_map[m]
        xn, yn = x + vx, y + vy

        if map_[yn][xn] == '#':
            continue

        if map_[yn][xn] == '.':
            map_[y][x], map_[yn][xn] = map_[yn][xn], map_[y][x]

        elif map_[yn][xn] in ('[', ']'):

            if vy == 0:
                px, py = walk(map_, xn, yn, vx, vy)

                if map_[py][px] == '#':
                    continue

                if map_[py][px] == '.':
                    shift(map_, x, y, px, py, vx, vy)

            elif vx == 0:
                if not walk_rec(map_, xn, yn, vy):
                    continue

                shift_rec(map_, xn, yn, vy)
                map_[y][x], map_[yn][xn] = map_[yn][xn], map_[y][x]

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