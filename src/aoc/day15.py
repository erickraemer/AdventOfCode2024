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
    while True:
        x, y = x + vx, y + vy

        if map_[y][x] in {'#', '.'}:
            return x, y

def shift( map_: list[list[chr]], x1: int, y1: int, x2: int, y2: int, vx: int, vy: int):
    if x1 > x2:
        x1, x2 = x2, x1

    if y1 > y2:
        y1, y2 = y2, y1

    buffer = [map_[y_][x_] for y_ in range(y1, y2+1) for x_ in range(x1, x2+1)]
    for i, c in enumerate(buffer):
        map_[y1 + (i + 1 * vy) % (y2 + 1 - y1)][x1 + (i + 1 * vx) % (x2 + 1 - x1)] = c

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

    sum_ = 0
    for y in range(len(map_)):
        for x in range(len(map_[y])):
            if map_[y][x] == 'O':
                sum_ += 100 * y + x

    return sum_

def part_two(file: Path):
    pass


def main():
    executor = Executor(
        test_file=DATA / "t15.txt",
        input_file=DATA / "i15.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(10092)
    executor.one("Box Score")

if __name__ == "__main__":
    main()