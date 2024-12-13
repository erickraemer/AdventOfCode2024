from pathlib import Path
from typing import Optional

import numpy as np

from common.executor import execute


def read_input(file: Path) -> np.ndarray:
    data: list[str] = open(file, "r").read().split()

    for i, d in enumerate(data):
        data[i] = [int(k) for k in d]

    arr = np.array(data, dtype=int)

    return arr

def in_bounds(coord: tuple, bounds: tuple) -> bool:
    assert len(coord) == len(bounds)

    return all(coord[i] in range(bounds[i]) for i in range(len(coord)))

def part_one_rec(data: np.ndarray, index: tuple[int, int], visited: Optional[set[tuple[int, int]]]) -> int:

    if visited is not None:
        if index in visited:
            return 0
        else:
            visited.add(index)

    value: int = data[index].item()
    if value == 9:
        return 1

    sum_: int = 0
    for c in ((0,1), (1,0), (-1,0), (0,-1)):
        next_ = tuple(np.array(index) + np.array(c))

        if not in_bounds(next_, data.shape):
            continue

        if data[next_] != value + 1:
            continue

        sum_ += part_one_rec(data, next_, visited)

    return sum_

def main(file: Path, task_one: bool) -> int:
    data = read_input(file)

    sum_: int = 0
    for y in range(len(data)):
        for x in range(len(data[y])):

            coord = (y, x)

            if data[coord] != 0:
                continue

            sum_ += part_one_rec(
                data,
                coord,
                set() if task_one else None
            )

    return sum_

def part_one(file: Path):
    return main(file, True)

def part_two(file: Path):
    return main(file, False)


if __name__ == "__main__":
    execute(
        Path("Day10/test.txt"),
        Path("Day10/input.txt"),
        part_one,
        36,
        "[1] Score"
    )

    execute(
        Path("Day10/test.txt"),
        Path("Day10/input.txt"),
        part_two,
        81,
        "[2] Checksum"
    )
