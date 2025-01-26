from copy import deepcopy
from pathlib import Path
from typing import Optional, Final

from aoc import DATA
from aoc.common.executor import Executor


def read_input(file: Path) -> list[str]:
    data = open(file, "r").read()
    data = data.split()

    return data


def in_bounds(coord: tuple, bounds: tuple) -> bool:
    assert len(coord) == len(bounds)

    return all(coord[i] in range(bounds[i]) for i in range(len(coord)))


def part_one_rec(
        y: int, x: int,
        data: list[str],
        visited: list[list[bool]],
        perimeter: Optional[list[list[int]]] = None,
        group: Optional[list[tuple[int, int]]] = None
):
    if group is None:
        group = []

    # add field to the current group and mark as visited
    group.append((y, x))
    visited[y][x] = True

    char: Final[chr] = data[y][x]
    bounds: Final[tuple[int, int]] = (len(data), len(data[0]))
    # check surrounding fields
    for (yn, xn) in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):

        inc_perimeter: bool = (
                not in_bounds((yn, xn), bounds) or
                data[yn][xn] != char
        )

        if inc_perimeter:
            if perimeter is not None:
                perimeter[y][x] += 1
            continue

        if visited[yn][xn]:
            continue

        part_one_rec(yn, xn, data, visited, perimeter, group)

    return group


def common(data: list[str], perimeter: list[list[int]], pt_one: bool):
    visited: list[list[bool]] = [[False] * len(d) for d in data]

    price: int = 0
    for y in range(len(data)):
        for x in range(len(data[0])):

            if visited[y][x]:
                continue

            group = part_one_rec(y, x, data, visited, perimeter if pt_one else None)

            p: int = sum(perimeter[yg][xg] for (yg, xg) in group)
            price += p * len(group)

    return price


def part_one(file: Path):
    data: Final[list[str]] = read_input(file)
    perimeter: list[list[int]] = [[0] * len(d) for d in data]

    return common(data, perimeter, True)


def detect_edge(x0: int, y0: int, pd: list[str], perimeter: list[list[int]], vertical: bool = False):
    x1: Final[int] = int(vertical)
    y1: Final[int] = int(not vertical)

    # no change
    if pd[y0][x0] == pd[y0 - y1][x0 - x1]:
        return

    b0: Final[bool] = pd[y0 - x1][x0 - y1] == pd[y0 - 1][x0 - 1]
    b1: Final[bool] = pd[y0][x0] != pd[y0 - x1][x0 - y1]
    b2: Final[bool] = pd[y0 - y1][x0 - x1] != pd[y0 - 1][x0 - 1]

    if b1 or (b0 and b2):
        perimeter[y0][x0] += 1

    if b2 or (b0 and b1):
        perimeter[y0 - y1][x0 - x1] += 1


def calculate_perimeter(data: list[str]):
    pd = deepcopy(data)

    # pad data array with a zero border
    for i in range(len(pd)):
        pd[i] = f"0{pd[i]}0"

    pd.insert(0, "".join(["0"] * len(pd[0])))
    pd.append(pd[0])

    # init perimeter array
    # note: using numpy here is slower than using lists
    perimeter = [[0] * len(d) for d in pd]

    # scan data array horizontally and vertically to detect edges
    for y in range(1, len(pd)):
        for x in range(1, len(pd[y])):
            # possible to vectorize this loop for a speedup
            detect_edge(x, y, pd, perimeter)
            detect_edge(x, y, pd, perimeter, True)

    # remove zero border of the perimeter array
    perimeter = [p[1:-1] for p in perimeter[1:-1]]

    return perimeter


def part_two(file: Path):
    data: Final[list[str]] = read_input(file)
    perimeter: list[list[int]] = calculate_perimeter(data)

    return common(data, perimeter, False)


def main():
    executor = Executor(
        test_file=DATA / "t12.txt",
        input_file=DATA / "i12.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(1930)
    executor.one("Price")

    executor.test_two(1206)
    executor.two("Price")


if __name__ == "__main__":
    main()
